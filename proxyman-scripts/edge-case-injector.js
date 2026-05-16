/**
 * Edge Case Injector Script for Basket API
 *
 * This script randomly injects problematic data to test input validation:
 * - Very long product names (100+ chars)
 * - Special characters (emoji, HTML, SQL injection)
 * - Negative prices or quantities
 * - Null/missing required fields
 * - Extremely high quantities
 * - Unicode edge cases
 * - Whitespace anomalies
 *
 * URL: https://api.staging.digital.rema1000.dk/api/v3/jobs/*/baskets/*
 */

async function onResponse(context, url, request, response) {
  // Only process basket endpoints with items
  if (!url.includes('/baskets/') || !response.body) {
    return response;
  }

  let json;
  try {
    json = JSON.parse(response.body);
  } catch (e) {
    return response;
  }

  if (!json.data || !json.data.items) {
    return response;
  }

  const edgeCases = [
    // 1. Very long product name (150+ characters)
    {
      id: 9900001,
      type: "default",
      name: "DETTE ER ET EKSTREMT LANGT PRODUKTNAVN SOM OVERSTIGER HUNDREDE TEGN FOR AT TESTE HVORDAN APPLIKATIONEN HÅNDTERER MEGET LANGE TEKSTSTRENGE I BRUGERGRÆNSEFLADEN OG POTENTIELT BRYDER LAYOUTET",
      underline: "999 KG. / DETTE ER OGSÅ EN MEGET LANG BESKRIVELSE SOM BURDE TESTE LAYOUT OG TEKSTHÅNDTERING I ALLE VIEWS",
      amount: 9999,
      price: 99999.99,
      barcode: "1234567890123456789012345678901234567890",
      product_id: 999999,
      job_item: {
        id: 9900001,
        name: "LANGT NAVN TEST",
        underline: "999 KG.",
        amount: 9999,
        product_id: 999999
      }
    },

    // 2. Emoji and XSS injection
    {
      id: 9900002,
      type: "default",
      name: "🍕 PIZZA MED EMOJI 🎉🔥💯 & <script>alert('XSS')</script>",
      underline: "<b>BOLD HTML</b> & <img src=x onerror=alert(1)>",
      amount: 5,
      price: 49.95,
      barcode: "emoji-test-123",
      product_id: 111111,
      job_item: {
        id: 9900002,
        name: "🍕 EMOJI TEST 🎉",
        underline: "<script>XSS</script>",
        amount: 5,
        product_id: 111111
      }
    },

    // 3. SQL Injection attempts
    {
      id: 9900003,
      type: "default",
      name: "SQL' OR '1'='1'; DROP TABLE products;--",
      underline: "Robert'); DROP TABLE items;--",
      amount: -5,
      price: -29.99,
      barcode: "'; DELETE FROM users;--",
      product_id: 222222,
      job_item: {
        id: 9900003,
        name: "SQL INJECTION TEST",
        underline: "NEGATIVE QTY & PRICE",
        amount: -5,
        product_id: 222222
      }
    },

    // 4. Null/missing fields
    {
      id: 9900004,
      type: "default",
      name: null,
      underline: null,
      amount: 0,
      price: 0,
      barcode: null,
      product_id: null,
      job_item: null
    },

    // 5. Empty strings
    {
      id: 9900005,
      type: "default",
      name: "",
      underline: "",
      amount: 1,
      price: 0.001,
      barcode: "",
      product_id: 0,
      job_item: {
        id: 0,
        name: "",
        underline: "",
        amount: 0,
        product_id: 0
      }
    },

    // 6. Integer overflow / boundary values
    {
      id: 9900006,
      type: "unknown_type",
      name: "BOUNDARY VALUE TEST",
      underline: "INTEGER OVERFLOW",
      amount: 2147483647,
      price: 1.7976931348623157e+308,
      barcode: "MAX_INT_TEST",
      product_id: -1,
      job_item: {
        id: -999,
        name: "OVERFLOW TEST",
        underline: "MAX VALUES",
        amount: -2147483648,
        product_id: -1
      }
    },

    // 7. Whitespace anomalies
    {
      id: 9900007,
      type: "self_scale",
      name: "     WHITESPACE     TEST     ",
      underline: "\t\n\r TABS AND NEWLINES \t\n\r",
      amount: 1,
      price: 10.00,
      barcode: "   ",
      product_id: 333333,
      job_item: {
        id: 9900007,
        name: "     SPACES     ",
        underline: "\t\n\r",
        amount: 1,
        product_id: 333333
      }
    },

    // 8. Unicode edge cases
    {
      id: 9900008,
      type: "default",
      name: "UNICODE: Ω≈ç√∫˜µ≤≥÷æ…¬˚∆˙©ƒ∂ßåΩ≈ç√∫˜µ",
      underline: "中文测试 العربية עברית 日本語 한국어",
      amount: 1,
      price: 123.45,
      barcode: "UNICODE✓✗★☆",
      product_id: 444444,
      job_item: {
        id: 9900008,
        name: "UNICODE ÆØÅ äöü",
        underline: "多语言测试",
        amount: 1,
        product_id: 444444
      }
    },

    // 9. Zero and decimal edge cases
    {
      id: 9900009,
      type: "default",
      name: "DECIMAL EDGE CASE",
      underline: "0.000001 KG",
      amount: 0,
      price: 0.000001,
      barcode: "0000000000000",
      product_id: 555555,
      job_item: {
        id: 9900009,
        name: "ZERO QTY",
        underline: "MICRO PRICE",
        amount: 0,
        product_id: 555555
      }
    },

    // 10. Special Danish characters stress test
    {
      id: 9900010,
      type: "default",
      name: "RØDGRØD MED FLØDE ÆBLESKIVER ØRRED ÅNGSTRÖM",
      underline: "ÆØÅ æøå ÅÅÅÅ ØØØØ ÆÆÆÆ",
      amount: 3,
      price: 42.00,
      barcode: "DK-ÆØÅ-123",
      product_id: 666666,
      job_item: {
        id: 9900010,
        name: "ÆØÅÆØÅÆØÅ",
        underline: "DANISH CHARS",
        amount: 3,
        product_id: 666666
      }
    }
  ];

  // Configuration: how many edge cases to inject (1-5 random)
  const numToInject = Math.floor(Math.random() * 5) + 1;

  // Shuffle and pick random edge cases
  const shuffled = edgeCases.sort(() => 0.5 - Math.random());
  const selectedCases = shuffled.slice(0, numToInject);

  // Inject edge cases into items array
  json.data.items = [...json.data.items, ...selectedCases];

  // Randomly corrupt total_price (20% chance)
  if (Math.random() < 0.2) {
    json.data.total_price = -Math.abs(json.data.total_price);
  }

  // Randomly corrupt shopper data (10% chance)
  if (Math.random() < 0.1 && json.data.shopper) {
    json.data.shopper.name = "<script>alert('XSS')</script>";
    json.data.shopper.email = "test'; DROP TABLE users;--";
    json.data.shopper.phone = "+45 99 99 99 99 99 99 99 99";
  }

  // Log what was injected (visible in Proxyman console)
  console.log(`[Edge Case Injector] Injected ${selectedCases.length} edge cases:`);
  selectedCases.forEach((item, i) => {
    console.log(`  ${i + 1}. ${item.name || '(null)'}`);
  });

  response.headers["X-Edge-Cases-Injected"] = selectedCases.length.toString();
  response.body = JSON.stringify(json);

  return response;
}
