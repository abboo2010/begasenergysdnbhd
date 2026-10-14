<?php
defined('_JEXEC') or die;
use Joomla\CMS\Uri\Uri;
$root = Uri::root(true) ?: '/';
?>
<!DOCTYPE html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title><?php echo (int) $this->error->getCode(); ?> | BEGAS Energy</title>
<link rel="stylesheet" href="<?php echo Uri::root(true); ?>/templates/begas/css/template.css"></head>
<body class="site"><main class="wrap content" style="padding:120px 32px">
<p class="eyebrow">Error <?php echo (int) $this->error->getCode(); ?></p>
<h1><?php echo (int) $this->error->getCode() === 404 ? 'This page could not be found.' : 'Something went wrong.'; ?></h1>
<p>Please return to the home page or contact us on +6088-486 262.</p>
<p><a class="btn btn-dark" href="<?php echo $root; ?>">Back to home</a></p>
</main></body></html>
