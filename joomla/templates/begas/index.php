<?php
/**
 * BEGAS Energy template (Joomla 4/5)
 */
defined('_JEXEC') or die;

use Joomla\CMS\Factory;
use Joomla\CMS\HTML\HTMLHelper;
use Joomla\CMS\Language\Text;
use Joomla\CMS\Uri\Uri;

/** @var Joomla\CMS\Document\HtmlDocument $this */
$app   = Factory::getApplication();
$wa    = $this->getWebAssetManager();
$tpath = Uri::root(true) . '/templates/' . $this->template;
$menu  = $app->getMenu()->getActive();
$home  = $menu && $menu->id == $app->getMenu()->getDefault()->id;

$wa->useStyle('template.begas');
$this->setMetaData('viewport', 'width=device-width, initial-scale=1');
$this->setMetaData('theme-color', '#071B2B');

$brand = htmlspecialchars($this->params->get('brandName', 'BEGAS'), ENT_QUOTES, 'UTF-8');
$tag   = htmlspecialchars($this->params->get('brandTag', 'ENERGY SDN BHD'), ENT_QUOTES, 'UTF-8');
$cta   = htmlspecialchars($this->params->get('ctaText', 'Request an Enquiry'), ENT_QUOTES, 'UTF-8');
$ctaLn = htmlspecialchars($this->params->get('ctaLink', '/index.php/contact-us'), ENT_QUOTES, 'UTF-8');
?>
<!DOCTYPE html>
<html lang="<?php echo $this->language; ?>" dir="<?php echo $this->direction; ?>">
<head>
    <jdoc:include type="metas" />
    <link rel="icon" href="<?php echo $tpath; ?>/favicon/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="<?php echo $tpath; ?>/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="<?php echo $tpath; ?>/favicon/favicon-16x16.png">
    <link rel="apple-touch-icon" href="<?php echo $tpath; ?>/favicon/apple-touch-icon.png">
    <jdoc:include type="styles" />
    <jdoc:include type="scripts" />
</head>
<body class="site <?php echo $home ? 'is-home' : 'is-inner'; ?>">
<a class="skip" href="#main"><?php echo Text::_('JSKIP_TO_CONTENT'); ?></a>

<header class="nav">
    <div class="wrap nav-in">
        <a class="brand" href="<?php echo Uri::root(true) ?: '/'; ?>" aria-label="<?php echo $brand . ' ' . $tag; ?>, home">
            <img src="<?php echo $tpath; ?>/images/begas-logo.png" alt="" width="69" height="46">
            <span class="brand-txt"><b><?php echo $brand; ?></b><span><?php echo $tag; ?></span></span>
        </a>
        <nav class="nav-links" aria-label="Primary">
            <jdoc:include type="modules" name="menu" style="none" />
        </nav>
        <a class="btn btn-sm nav-cta" href="<?php echo $ctaLn; ?>"><?php echo $cta; ?></a>
        <button class="burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu">
            <svg width="22" height="22" viewBox="0 0 22 22" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 6h16M3 11h16M3 16h16"/></svg>
        </button>
    </div>
    <div class="mpanel" id="mobile-menu" hidden></div>
</header>

<?php if ($this->countModules('banner')) : ?>
<div class="banner"><jdoc:include type="modules" name="banner" style="none" /></div>
<?php endif; ?>

<main id="main">
    <?php if ($this->countModules('breadcrumbs')) : ?>
    <div class="wrap crumbs-wrap"><jdoc:include type="modules" name="breadcrumbs" style="none" /></div>
    <?php endif; ?>
    <jdoc:include type="modules" name="main-top" style="none" />
    <div class="wrap content">
        <jdoc:include type="message" />
        <jdoc:include type="component" />
    </div>
    <jdoc:include type="modules" name="main-bottom" style="none" />
    <?php if ($this->countModules('cta')) : ?>
    <section class="cta"><div class="wrap cta-in"><jdoc:include type="modules" name="cta" style="none" /></div></section>
    <?php endif; ?>
</main>

<footer class="foot">
    <div class="wrap">
        <div class="foot-grid">
            <div><jdoc:include type="modules" name="footer-1" style="none" /></div>
            <div><jdoc:include type="modules" name="footer-2" style="none" /></div>
            <div><jdoc:include type="modules" name="footer-3" style="none" /></div>
            <div><jdoc:include type="modules" name="footer-4" style="none" /></div>
        </div>
        <div class="foot-bar">
            <span>&copy; <?php echo date('Y'); ?> BEGAS Energy Sdn Bhd. All rights reserved.</span>
            <jdoc:include type="modules" name="footer-bar" style="none" />
        </div>
    </div>
</footer>

<script>
(function () {
  var b = document.querySelector('.burger'), p = document.getElementById('mobile-menu'),
      src = document.querySelector('.nav-links');
  if (!b || !p || !src) return;
  p.innerHTML = src.innerHTML;
  b.addEventListener('click', function () {
    var open = b.getAttribute('aria-expanded') === 'true';
    b.setAttribute('aria-expanded', String(!open));
    b.setAttribute('aria-label', open ? 'Open menu' : 'Close menu');
    p.hidden = open;
  });
})();
</script>
<jdoc:include type="modules" name="debug" style="none" />
</body>
</html>
