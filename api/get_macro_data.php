<?php

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

header('Content-Type: application/json; charset=utf-8');
//header('Cache-Control: no-cache, must-revalidate');

$dbPath = dirname(__DIR__) . '/data/montco_estate/montco_macro.db';

if (!file_exists($dbPath)) {
  //http_response_code(500);
  echo json_encode([
                     'error' => 'Database file not found at : ',
                     'attempted path' => $dbPath,
                     'current_dir' => __DIR__
                     ]);
  exit;
}

try {

  $db = new PDO('sqlite:' . $dbPath, null, null, [
                  PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                  PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
                  ]);

  // FIX 1: Added 'date' to the SELECT statement
  $stmt = $db->query("SELECT date, MORTGAGE30US, CPIAUCSL FROM montco_monthly ORDER BY date ASC");
  $rows = $stmt->fetchAll();

  $dates = [];
  $mortgageRates = [];
  $cpiValues = [];

  // FIX 2: Added the missing $ before row
  foreach ($rows as $row) {
    $dates[] = $row['date'];
    $mortgageRates[] = isset($row['MORTGAGE30US']) ? (float)$row['MORTGAGE30US'] : null;
    $cpiValues[] = isset($row['CPIAUCSL']) ? (float)$row['CPIAUCSL']: null;
  }

  echo json_encode([
                     'dates' => $dates,
                     // FIX 3: Spelled 'mortgage_rates' correctly to match frontend JS
                     'mortgage_rates' => $mortgageRates, 
                     'cpi' => $cpiValues
  ]);

} catch (PDOException $e) {
  http_response_code(500);
  echo json_encode(['error' => 'Database Error ' . $e->getMessage()]);
}
