/**
 * Organization Calendar Search
 * Searches for a specific meeting title across all people in your Google Workspace org.
 *
 * SETUP:
 * 1. Create a new Google Sheet → Extensions → Apps Script
 * 2. Paste this entire script
 * 3. In Apps Script: Services (+ icon on left) → add "People API" AND "Google Calendar API"
 * 4. Run → searchMeeting() → Authorize when prompted
 * 5. Results appear in the spreadsheet
 */

// ============================
// CONFIGURATION — edit these
// ============================
const CONFIG = {
  // Search terms — matches ANY of these (case-insensitive, partial match)
  searchTerms: [
    "Company update regarding your position",
    "Virksomhedsopdatering vedrørende din stilling",
    "Opdatering vedrørende din stilling",
  ],
  emailDomain: "framna.com",        // Only scan people with this email domain
  daysAhead: 60,                    // How many days ahead to search
  daysBack: 30,                     // How many days back to search
  maxPeople: 500,                   // Max org members to scan (safety limit)
};

// ============================
// MAIN FUNCTION
// ============================
function searchMeeting() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  sheet.clear();

  // Header row
  sheet.appendRow(["Name", "Email", "Meeting Title", "Date", "Start Time", "End Time", "Status"]);
  sheet.getRange(1, 1, 1, 7).setFontWeight("bold").setBackground("#4285f4").setFontColor("white");

  const ui = SpreadsheetApp.getUi();

  // Status cell
  sheet.getRange("I1").setValue("Searching...").setFontColor("orange");
  sheet.getRange("I2").setValue("Domain: " + CONFIG.emailDomain);
  sheet.getRange("I3").setValue("Terms: " + CONFIG.searchTerms.join(" | "));

  const people = getOrgPeople_();
  sheet.getRange("I1").setValue("Scanning " + people.length + " @" + CONFIG.emailDomain + " people...").setFontColor("orange");
  SpreadsheetApp.flush();

  const now = new Date();
  const startDate = new Date(now.getTime() - CONFIG.daysBack * 86400000);
  const endDate = new Date(now.getTime() + CONFIG.daysAhead * 86400000);

  let matchCount = 0;
  let scannedCount = 0;
  let skippedCount = 0;

  for (const person of people) {
    scannedCount++;

    // Update status every 10 people
    if (scannedCount % 10 === 0) {
      sheet.getRange("I1").setValue("Scanning " + scannedCount + "/" + people.length + "...");
      SpreadsheetApp.flush();
    }

    try {
      const events = findEventsForUser_multi_(person.email, CONFIG.searchTerms, startDate, endDate);

      for (const event of events) {
        matchCount++;
        sheet.appendRow([
          person.name,
          person.email,
          event.title,
          event.date,
          event.startTime,
          event.endTime,
          event.status
        ]);
      }
    } catch (e) {
      skippedCount++;
      Logger.log("Skipped " + person.email + ": " + e.message);
    }

    // Small delay to avoid rate limits
    if (scannedCount % 50 === 0) {
      Utilities.sleep(1000);
    }
  }

  // Summary
  sheet.getRange("I1").setValue("Done!").setFontColor("green");
  sheet.getRange("I2").setValue("People scanned: " + scannedCount);
  sheet.getRange("I3").setValue("Matches found: " + matchCount);
  sheet.getRange("I4").setValue("Skipped (no access): " + skippedCount);

  // Auto-resize columns
  for (let i = 1; i <= 7; i++) {
    sheet.autoResizeColumn(i);
  }

  ui.alert(
    "Search Complete",
    "Found " + matchCount + " matching events across " + scannedCount +
    " people.\n\nSkipped " + skippedCount + " (no calendar access).",
    ui.ButtonSet.OK
  );
}

// ============================
// DIRECTORY LOOKUP
// ============================
function getOrgPeople_() {
  const people = [];
  let pageToken = null;

  do {
    const params = {
      readMask: "names,emailAddresses",
      sources: ["DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE"],
      pageSize: 200,
    };
    if (pageToken) params.pageToken = pageToken;

    const response = People.People.listDirectoryPeople(params);

    if (response.people) {
      for (const person of response.people) {
        const name = (person.names && person.names[0])
          ? person.names[0].displayName
          : "Unknown";
        const email = (person.emailAddresses && person.emailAddresses[0])
          ? person.emailAddresses[0].value
          : null;

        if (email && email.toLowerCase().endsWith("@" + CONFIG.emailDomain)) {
          people.push({ name, email });
        }
      }
    }

    pageToken = response.nextPageToken || null;
  } while (pageToken && people.length < CONFIG.maxPeople);

  Logger.log("Found " + people.length + " people in org directory");
  return people;
}

// ============================
// CALENDAR SEARCH (multi-term)
// ============================
function findEventsForUser_multi_(email, searchTerms, startDate, endDate) {
  const results = [];
  const seenKeys = new Set(); // deduplicate across search terms
  const tz = Session.getScriptTimeZone();

  for (const searchTerm of searchTerms) {
    try {
      const response = Calendar.Events.list(email, {
        q: searchTerm,
        timeMin: startDate.toISOString(),
        timeMax: endDate.toISOString(),
        singleEvents: true,
        orderBy: "startTime",
        maxResults: 50,
      });

      if (response.items) {
        for (const event of response.items) {
          if (!event.summary) continue;

          // Check if title matches ANY of the search terms
          const titleLower = event.summary.toLowerCase();
          const matches = searchTerms.some(function(term) {
            return titleLower.includes(term.toLowerCase());
          });
          if (!matches) continue;

          // Deduplicate by event ID
          const key = event.id + "_" + (event.start.dateTime || event.start.date);
          if (seenKeys.has(key)) continue;
          seenKeys.add(key);

          const start = event.start.dateTime
            ? new Date(event.start.dateTime)
            : new Date(event.start.date);
          const end = event.end.dateTime
            ? new Date(event.end.dateTime)
            : new Date(event.end.date);

          results.push({
            title: event.summary,
            date: Utilities.formatDate(start, tz, "yyyy-MM-dd"),
            startTime: event.start.dateTime
              ? Utilities.formatDate(start, tz, "HH:mm")
              : "All day",
            endTime: event.end.dateTime
              ? Utilities.formatDate(end, tz, "HH:mm")
              : "All day",
            status: event.status || "confirmed",
          });
        }
      }
    } catch (e) {
      // If one search term fails, continue with the others
      Logger.log("Search term '" + searchTerm + "' failed for " + email + ": " + e.message);
    }
  }

  return results;
}

// ============================
// MENU
// ============================
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("Calendar Search")
    .addItem("Search for Meeting", "searchMeeting")
    .addToMenu();
}
