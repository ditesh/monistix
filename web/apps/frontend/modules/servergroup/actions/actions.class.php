<?php

/**
 * servergroup actions.
 *
 * @package    monistix
 * @subpackage servergroup
 * @author     Your name here
 * @version    SVN: $Id: actions.class.php 23810 2009-11-12 11:07:44Z Kris.Wallsmith $
 */
class servergroupActions extends sfActions
{
  public function executeIndex(sfWebRequest $request)
  {
    $this->server_groups = Doctrine_Core::getTable('ServerGroup')
      ->createQuery('a')
      ->execute();
  }

  public function executeShow(sfWebRequest $request)
  {
    $this->server_group = Doctrine_Core::getTable('ServerGroup')->find(array($request->getParameter('id')));
    $this->forward404Unless($this->server_group);
  }

  public function executeNew(sfWebRequest $request)
  {
    $this->form = new ServerGroupForm();
  }

  public function executeCreate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST));

    $this->form = new ServerGroupForm();

    $this->processForm($request, $this->form);

    $this->setTemplate('new');
  }

  public function executeEdit(sfWebRequest $request)
  {
    $this->forward404Unless($server_group = Doctrine_Core::getTable('ServerGroup')->find(array($request->getParameter('id'))), sprintf('Object server_group does not exist (%s).', $request->getParameter('id')));
    $this->form = new ServerGroupForm($server_group);
  }

  public function executeUpdate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST) || $request->isMethod(sfRequest::PUT));
    $this->forward404Unless($server_group = Doctrine_Core::getTable('ServerGroup')->find(array($request->getParameter('id'))), sprintf('Object server_group does not exist (%s).', $request->getParameter('id')));
    $this->form = new ServerGroupForm($server_group);

    $this->processForm($request, $this->form);

    $this->setTemplate('edit');
  }

  public function executeDelete(sfWebRequest $request)
  {
    $request->checkCSRFProtection();

    $this->forward404Unless($server_group = Doctrine_Core::getTable('ServerGroup')->find(array($request->getParameter('id'))), sprintf('Object server_group does not exist (%s).', $request->getParameter('id')));
    $server_group->delete();

    $this->redirect('servergroup/index');
  }

  protected function processForm(sfWebRequest $request, sfForm $form)
  {
    $form->bind($request->getParameter($form->getName()), $request->getFiles($form->getName()));
    if ($form->isValid())
    {
      $server_group = $form->save();

      $this->redirect('server/index?group='.$server_group->getId());
    }
  }
}
