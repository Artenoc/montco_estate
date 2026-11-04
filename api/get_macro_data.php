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


  $stmt = $db->query("SELECT date, mortgage_rate, cpi FROM montco_monthly ORDER BY date ASC");
  $rows = $stmt->fetchAll();

  $dates = [];
  $mortgageRates = [];
  $cpiValues = [];

  foreach ($rows as $row) {
    $dates[] = $row['date'];
    $mortgageRates[] = isset($row['mortgage_rate']) ? (float)$row['mortgage_rate'] : null;
    $cpiValues[] = isset($row['cpi']) ? (float)$row['cpi']: null;
  }

  echo json_encode([
                     'dates' => $dates,
                     'mortgage_rates' => $mortgageRates, 
                     'cpi' => $cpiValues
  ]);

} catch (PDOException $e) {
  http_response_code(500);
  echo json_encode(['error' => 'Database Error ' . $e->getMessage()]);
}
