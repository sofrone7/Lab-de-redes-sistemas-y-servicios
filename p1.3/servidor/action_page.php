<?php
echo '<!DOCTYPE html>';
echo '<html>';
echo '<body>';
echo '<form action="/action_page.php">';
echo 'Time:<br>';
echo '<input type="text" name="Time" value=" ">';
echo '<br>';
echo 'Draw Time:<br>';
echo '<input type="text" name="Draw Time" value=" ">';
echo '<br>';
echo 'AP:<br>';
echo '<input type="text" name="AP" value=" ">';
echo '<br>';
echo 'JP:<br>';
echo '<input type="text" name="JP" value=" ">';
echo '<br>';
echo 'S7:<br>';
echo '<input type="text" name="7S" value=" ">';
echo '<br><br>';
echo '<input type="submit" value="Submit">';
echo '</form>';
echo '<p>If you click the "Submit" button, the form-data will be sent to a page called "/action_page.php".</p>';
echo '</body>';
echo '</html>';
echo '';
?>
