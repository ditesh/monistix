<?php

class serverComponents extends sfComponents {

  public function executeSidebar(sfWebRequest $request)
  {
    $this->groups = Doctrine_Core::getTable('ServerGroup')->getWithServers();
    $groupID = $request->getParameter("group");
    if (strlen($groupID) > 0 && ctype_digit($groupID)) {
	$this->groupID = $groupID;
    }
  }
}

?>
