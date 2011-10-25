<?php use_stylesheets_for_form($form) ?>
<?php use_javascripts_for_form($form) ?>

<form action="<?php echo url_for('servergroup/'.($form->getObject()->isNew() ? 'create' : 'update').(!$form->getObject()->isNew() ? '?id='.$form->getObject()->getId() : '')) ?>" method="post" <?php $form->isMultipart() and print 'enctype="multipart/form-data" ' ?>>

	<?php if ($form->hasErrors()): ?>
	<ul class="error">
		<strong>Errors:</strong>
		<?php foreach($form->getWidgetSchema()->getPositions() as $widgetName): ?>
		<?php if ($form[$widgetName]->hasError()): ?>
		<li class="error-item">
		<?php echo $form[$widgetName]->renderLabelName()." ".strtolower($form[$widgetName]->getError()) ?>
		</li>
		<?php endif ?>
		<?php endforeach ?>
	</ul>
	<?php endif ?>

	<?php if (!$form->getObject()->isNew()): ?>
	<input type="hidden" name="sf_method" value="put" />
	<?php endif; ?>

	<?php foreach ($form as $widget): ?>

		<?php if ($widget->getName() == "_csrf_token"): ?>
		<?php continue ?>
		<?php endif ?>

		<div class="form-label">
			<?php echo $widget->renderLabel() ?>
		</div>
		<div class="form-widget">
			<?php echo $widget->render()  ?>
		</div>

	<?php endforeach ?>

	<?php if (!$form->getObject()->isNew()): ?>
	<?php $js = _convert_options_to_javascript(array('method' => 'delete', 'confirm' => 'Are you sure?'), 'server/delete?id='.$form->getObject()->getId()) ?>
	<input type="button" class="button-red" value="Delete" onclick="<?php echo $js["onclick"] ?>">
	<?php endif; ?>

	<?php echo $form[$form->getCSRFFieldName()]->render() ?>

	<input class="button" type="submit" value="Save">

</form>
