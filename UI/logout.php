<?php
/*
Author: Javed Ur Rehman
Website: https://htmlcssphptutorial.wordpress.com
*/
?>

<?php
session_start();
if(session_destroy()) // Destroying All Sessions
{
header("Location: frontend.php"); // Redirecting To Home Page
}
?>