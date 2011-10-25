<div>
  <h1>Organizations</h1>
    <div>

	<?php if (isset($organizationID)): ?>
	<div class="category" id="category-0">
	<?php else: ?>
	<div class="category selected" id="category-0">
	<?php endif ?>
		<?php echo link_to("All organizations", 'organization/index') ?>
	</div>

	<?php foreach($organizations as $organization): ?>
	<?php if ($organization->getId() == $sf_request->getParameter("organization")): ?>
	<div class="category selected" id="category-<?php echo $organization->getId() ?>"><?php echo link_to($organization->getName(),'organization/index?organization='.$organization->getId()) ?></div>
	<?php else: ?>
	<div class="category" id="category-<?php echo $organization->getId() ?>"><?php echo link_to($organization->getName(),'organization/index?organization='.$organization->getId()) ?></div>
	<?php endif ?>
	<?php if ($organization->getId() == $sf_request->getParameter("id")): ?>
		<div class="category-contents" style="display: block" id="category-contents-<?php echo $organization->getId() ?>">
	<?php else: ?>
		<div class="category-contents" id="category-contents-<?php echo $organization->getId() ?>">
	<?php endif ?>
		<ul>
			<?php foreach($organization->getServers() as $server): ?>
			<li class="category-contents-item">
				<?php echo $server->getHostname() ?>
				<div class="right">
					<a class="button" href="/frontend_dev.php/server/new">Edit</a>
				</div>
			</li>
			<?php endforeach ?>
		</ul>
	</div>
	<?php endforeach ?>
    <div>
</div>
