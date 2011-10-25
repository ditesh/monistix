<?php

/**
 * server actions.
 *
 * @package    monistix
 * @subpackage server
 * @author     Ditesh Shashikant Gathani
 * @version    SVN: $Id: actions.class.php 23810 2009-11-12 11:07:44Z Kris.Wallsmith $
 */
class serverActions extends sfActions
{
  public function executeIndex(sfWebRequest $request)
  {
    $groupID = $request->getParameter("group");

    if (strlen($groupID)) {

	    $this->group= Doctrine_Core::getTable('ServerGroup')->find(array($groupID));
	    $this->forward404Unless($this->group);

	    $this->servers = Doctrine_Core::getTable('Server')
	      ->createQuery('a')
	      ->where('group_id=?', array($groupID))
	      ->execute();
    } else {

	    $this->servers = Doctrine_Core::getTable('Server')
	      ->createQuery('a')
	      ->execute();
    }
  }

  public function executeShow(sfWebRequest $request)
  {
    $this->server = Doctrine_Core::getTable('Server')->find(array($request->getParameter('id')));
    $this->forward404Unless($this->server);
  }

  public function executeNew(sfWebRequest $request)
  {
    $this->form = new ServerForm();
  }

  public function executeCreate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST));

    $this->form = new ServerForm();

    $this->processForm($request, $this->form);

    $this->setTemplate('new');
  }

  public function executeEdit(sfWebRequest $request)
  {
    $this->forward404Unless($server = Doctrine_Core::getTable('Server')->find(array($request->getParameter('id'))), sprintf('Object server does not exist (%s).', $request->getParameter('id')));
    $this->form = new ServerForm($server);
  }

  public function executeUpdate(sfWebRequest $request)
  {
    $this->forward404Unless($request->isMethod(sfRequest::POST) || $request->isMethod(sfRequest::PUT));
    $this->forward404Unless($server = Doctrine_Core::getTable('Server')->find(array($request->getParameter('id'))), sprintf('Object server does not exist (%s).', $request->getParameter('id')));
    $this->form = new ServerForm($server);

    $this->processForm($request, $this->form);

    $this->setTemplate('edit');
  }

  public function executeDelete(sfWebRequest $request)
  {
    $request->checkCSRFProtection();

    $this->forward404Unless($server = Doctrine_Core::getTable('Server')->find(array($request->getParameter('id'))), sprintf('Object server does not exist (%s).', $request->getParameter('id')));
    $server->delete();

    $this->redirect('server/index');
  }

  protected function processForm(sfWebRequest $request, sfForm $form)
  {
    $form->bind($request->getParameter($form->getName()), $request->getFiles($form->getName()));
    if ($form->isValid())
    {
      $server = $form->save();

      $this->redirect('server/index');
    }
  }
}
