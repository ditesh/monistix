<?php

/**
 * BaseOrganization
 * 
 * This class has been auto-generated by the Doctrine ORM Framework
 * 
 * @property string $name
 * @property boolean $enabled
 * @property string $notes
 * @property Doctrine_Collection $Organizations
 * 
 * @method string              getName()          Returns the current record's "name" value
 * @method boolean             getEnabled()       Returns the current record's "enabled" value
 * @method string              getNotes()         Returns the current record's "notes" value
 * @method Doctrine_Collection getOrganizations() Returns the current record's "Organizations" collection
 * @method Organization        setName()          Sets the current record's "name" value
 * @method Organization        setEnabled()       Sets the current record's "enabled" value
 * @method Organization        setNotes()         Sets the current record's "notes" value
 * @method Organization        setOrganizations() Sets the current record's "Organizations" collection
 * 
 * @package    monistix
 * @subpackage model
 * @author     Your name here
 * @version    SVN: $Id: Builder.php 7490 2010-03-29 19:53:27Z jwage $
 */
abstract class BaseOrganization extends sfDoctrineRecord
{
    public function setTableDefinition()
    {
        $this->setTableName('organization');
        $this->hasColumn('name', 'string', 255, array(
             'type' => 'string',
             'notnull' => true,
             'length' => 255,
             ));
        $this->hasColumn('enabled', 'boolean', null, array(
             'type' => 'boolean',
             'notnull' => true,
             'default' => true,
             ));
        $this->hasColumn('notes', 'string', null, array(
             'type' => 'string',
             ));
    }

    public function setUp()
    {
        parent::setUp();
        $this->hasMany('Project as Organizations', array(
             'local' => 'id',
             'foreign' => 'organization_id'));

        $timestampable0 = new Doctrine_Template_Timestampable();
        $this->actAs($timestampable0);
    }
}