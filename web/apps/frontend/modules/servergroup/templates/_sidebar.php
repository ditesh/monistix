<div>
  <h1>Server Groups</h1>
    <div>
        <div class="category" id="category-0">
                <?php echo link_to("All servers", 'server/index') ?>
        </div>

	<?php foreach($groups as $group): ?>
	<div class="category"><?php echo link_to($group->getName(),'server/index?group='.$group->getId()) ?></div>
	<div class="category-contents" id="category-contents-<?php echo $group->getId() ?>">
		<ul>
			<?php foreach($group->getServers() as $server): ?>
			<li class="category-contents-item">
				<?php echo $server->getHostname() ?>
			</li>
			<?php endforeach ?>
		</ul>
	</div>
	<?php endforeach ?>
    <div>
</div>
