<!DOCTYPE html>
<html>
  <head>
    <?php include_http_metas() ?>
    <?php include_metas() ?>
    <title>
	<?php include_slot('title', 'Monistix') ?>
    </title>
    <link rel="shortcut icon" href="/favicon.ico" />
    <?php include_stylesheets() ?>
    <?php include_javascripts() ?>
    </head>
    <body>
    <header>
	<div id="header-box-left">
		<a class="logo" href="http://monistix.com/">
			monistix
		</a>
	</div>
	<div id="header-box-right">
		<div class="name">Ditesh Shashikant Gathani</div>
		<ul>
			<li>
				<a href="/alerts">Alerts</a>
				<a href="" class="number">0</a>
			</li>
			<li><a href="/settings">Account Settings</a></li>
			<li><a href="/logout">Log Out</a></li>
		</ul>
	</div>
    </header>
    <nav>
	    <ul>
	        <?php if ($sf_context->getModuleName() == "dashboard"): ?>
	        <li><a class="selected" href="">Dashboard</a></li>
		<?php else: ?>
	        <li><a href="">Dashboard</a></li>
		<?php endif ?>

	        <li><a href="">Reports</a></li>

	        <?php if ($sf_context->getModuleName() == "server" || $sf_context->getModuleName() == "servergroup"): ?>
	        <li><a class="selected" href="<?php echo url_for("server/index") ?>">Servers</a></li>
		<?php else: ?>
	        <li><a href="<?php echo url_for("server/index") ?>">Servers</a></li>
		<?php endif ?>

	        <?php if ($sf_context->getModuleName() == "plugin"): ?>
	        <li><a class="selected" href="<?php echo url_for("plugin/index") ?>">Plugins</a></li>
		<?php else: ?>
	        <li><a href="<?php echo url_for("plugin/index") ?>">Plugins</a></li>
		<?php endif ?>

	        <?php if ($sf_context->getModuleName() == "organization"): ?>
	        <li><a class="selected" href="<?php echo url_for("organization/index") ?>">Organizations and Projects</a></li>
		<?php else: ?>
	servergroup        <li><a href="<?php echo url_for("organization/index") ?>">Organizations and Projects</a></li>
		<?php endif ?>

	        <li><a href="">Users and Groups</a></li>
	    <ul>
    </nav>
    <section id="content">
        <aside id="sidebar">
	    <?php if ($sf_context->getModuleName() == "server"): ?>
	    <?php include_component('server', 'sidebar') ?>
	    <?php elseif ($sf_context->getModuleName() == "servergroup"): ?>
	    <?php include_component('servergroup', 'sidebar') ?>
	    <?php elseif ($sf_context->getModuleName() == "organization"): ?>
	    <?php include_component('organization', 'sidebar') ?>
	    <?php endif ?>
	</aside>
        <section id="content-right">
	    <?php echo $sf_content ?>
        </section>
    </section>
    <footer>
	Monistix Systems Sdn Bhd (c) 2010
    </footer>
  </body>
</html>
