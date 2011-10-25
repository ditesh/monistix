<?php

/**
 * organization actions.
 *
 * @package    monistix
 * @subpackage server
 * @author     Ditesh Shashikant Gathani
 * @version    SVN: $Id: actions.class.php 23810 2009-11-12 11:07:44Z Kris.Wallsmith $
 */
class organizationActions extends sfActions
{
 /**
  * Executes index action
  *
  * @param sfRequest $request A request object
  */
  public function executeIndex(sfWebRequest $request)
  {

    $this->organizations = Doctrine_Core::getTable('Organization')
      ->createQuery('a')
      ->execute();
  }
}
