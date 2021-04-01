
<html>
    <head>
        <title>My Obsertory</title>
    </head>

    <body>
        <h1>Welcome to my observatory!!</h1>
        <ul>
            <?php
            # $json = file_get_contents('http://observatory-service/');
            $json = file_get_contents('http://backend-py/api/galaxies');
            $obj = json_decode($json);
            $galaxies = $obj->Galaxies;
            foreach ($galaxies as $galaxy) {
                echo "<li>$galaxy</li>";
            }
            ?>
        </ul>
    </body>
</html>
