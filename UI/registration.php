<?php
/*
Author: Javed Ur Rehman
Website: https://htmlcssphptutorial.wordpress.com
*/
?>

<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Registration</title>
<link rel="shortcut icon" type="image/png" href="/favicon.png"/>
<link rel="stylesheet" href="css/style.css" />
</head>
<body>
<?php
	/*require('db.php');*/
    // If form submitted, insert values into the database.1
    $conn = mysqli_connect(getenv('IP'),getenv('C9_USER'), "","c9",3306);
    if (isset($_POST['username'])){
        $username = $_POST['username'];
		$email = $_POST['email'];
        $password = $_POST['password'];
		$username = stripslashes($username);
		$username = mysqli_real_escape_string($conn,$_POST['username']);
		$email = stripslashes($email);
		$email = mysqli_real_escape_string($conn,$_POST['email']);
		$password = stripslashes($password);
		$password = mysqli_real_escape_string($conn,$_POST['password']);
		$trn_date = date("Y-m-d H:i:s");
        $query = "INSERT into `users` (username, password, email, trn_date) VALUES ('$username', '".md5($password)."', '$email', '$trn_date')";
        $result = mysqli_query($conn,$query);
        if($result){
            echo "<div class='form'><h3>You are registered successfully.</h3><br/>Click here to <a href='login.php'>Login</a></div>";
        }
    }else{
?>
<div class="form">
<h1>Registration</h1>
<form name="registration" action="" method="post">
<input type="text" autocomplete="off" name="username" placeholder="Username" required />
<input type="email" autocomplete="off" name="email" placeholder="Email" required />
<input type="password" autocomplete="off" name="password" placeholder="Password" required />
<input type="submit" name="submit" value="Register" />
</form>
</div>
<?php } ?>
</body>
</html>
