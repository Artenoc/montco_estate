<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-cache, must-revalidate');

try {
  $db = new PDO('sqlite:montco_macro.db');
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

  $stmt = $db->query('SELECT * FROM duplex_timeline ORDER BY date ASC')
  $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

  echo json_encode ([
                    'status' => 'success',
                    'count' => count($data),
                    'data' => $data
                    ]);
} catch (PDOException $e) {
  http_response_code(500);
  echo json_encode([
                   'status' => 'error',
                   'message' => $e->getMessage()
                   ]);
}
?>
