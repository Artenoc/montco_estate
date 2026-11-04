<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Cache-Control: no-cahce, must-revalidate');

try {
    $db = new PDO('sqlite:.../montco_macro.db')
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $smst = $db->query('SELECT * FROM duplex_timeline ORDER BY date ASC');
    $data = $smst->fetchAll(PDO::FETCH_ASSOC);

    echo json_encode([
        'status' => 'sucess',
        'count' => count($data),
        'data' => $data
        ]);
    } catch (PDOException $e){
        echo json_encode([
            'status' => 'error',
            'message' => $e->getMessage()
        ]);
    }
?>