<?php

namespace Monistix\OrganizationBundle\Entity;

use Doctrine\ORM\Mapping as ORM;
use Symfony\Component\Validator\Constraints as Assert;
use Doctrine\Common\Collections\ArrayCollection;

/**
 * @ORM\Entity
 * @ORM\Table(name="organization")
 */

class Organization {

    /**
     * @ORM\Id
     * @ORM\Column(type="integer")
     * @ORM\GeneratedValue(strategy="AUTO")
     */
    protected $id;

    /**
     * @ORM\Column(type="string", length=1024)
     * @Assert\NotBlank
     */
    protected $name;

    /**
     * @ORM\Column(type="integer", nullable=true)
     */
    protected $max_hosts;

    /**
     * @ORM\Column(type="integer", nullable=true)
     */
    protected $max_accounts;

    /**
     * @ORM\Column(type="boolean")
     */
    protected $accounts_active = true;

    /**
     * @ORM\Column(type="boolean")
     */
    protected $hosts_active = true;

    /**
     * @ORM\Column(type="boolean")
     */
    protected $enable_billing = false;

    /**
     * @ORM\Column(type="string", nullable=true, length=1024)
     */
    protected $billing_address;

    /**
     * @ORM\Column(type="string", nullable=true, length=1024)
     */
    protected $mailing_address;

    /**
     * @ORM\Column(type="string", nullable=true, length=1024)
     */
    protected $contact_name;

    /**
     * @ORM\Column(type="string", nullable=true, length=1024)
     */
    protected $contact_number;

    /**
     * @ORM\Column(type="string", nullable=true, length=1024)
     * @Assert\Email(
     *     message = "The email '{{ value }}' is not a valid email address.",
     *     checkMX = true)
     */
    protected $contact_email;

    /**
     * @ORM\Column(type="string", nullable=true, length=4096)
     */
    protected $miscellaneous;

    /**
     * @ORM\OneToMany(targetEntity="Project", mappedBy="organization", cascade={"persist", "remove"})
     *
     * @var ArrayCollection $projects
     */
    protected $projects;

    public function __construct() {
        $this->projects = new ArrayCollection();
    }

    public function getProjects() {
        return $this->projects;
    }

    public function setProjects(ArrayCollection $projects) {
        $this->projects = $projects;
    }


    /**
     * Get id
     *
     * @return integer 
     */
    public function getId()
    {
        return $this->id;
    }

    /**
     * Set name
     *
     * @param string $name
     */
    public function setName($name)
    {
        $this->name = $name;
    }

    /**
     * Get name
     *
     * @return string 
     */
    public function getName()
    {
        return $this->name;
    }

    /**
     * Set max_hosts
     *
     * @param integer $maxHosts
     */
    public function setMaxHosts($maxHosts)
    {
        $this->max_hosts = $maxHosts;
    }

    /**
     * Get max_hosts
     *
     * @return integer 
     */
    public function getMaxHosts()
    {
        return $this->max_hosts;
    }

    /**
     * Set max_accounts
     *
     * @param integer $maxAccounts
     */
    public function setMaxAccounts($maxAccounts)
    {
        $this->max_accounts = $maxAccounts;
    }

    /**
     * Get max_accounts
     *
     * @return integer 
     */
    public function getMaxAccounts()
    {
        return $this->max_accounts;
    }

    /**
     * Set active
     *
     * @param boolean $active
     */
    public function setActive($active)
    {
        $this->active = $active;
    }

    /**
     * Get active
     *
     * @return boolean 
     */
    public function getActive()
    {
        return $this->active;
    }

    /**
     * Set address
     *
     * @param string $address
     */
    public function setAddress($address)
    {
        $this->address = $address;
    }

    /**
     * Get address
     *
     * @return string 
     */
    public function getAddress()
    {
        return $this->address;
    }

    /**
     * Set contact_name
     *
     * @param string $contactName
     */
    public function setContactName($contactName)
    {
        $this->contact_name = $contactName;
    }

    /**
     * Get contact_name
     *
     * @return string 
     */
    public function getContactName()
    {
        return $this->contact_name;
    }

    /**
     * Set contact_number
     *
     * @param string $contactNumber
     */
    public function setContactNumber($contactNumber)
    {
        $this->contact_number = $contactNumber;
    }

    /**
     * Get contact_number
     *
     * @return string 
     */
    public function getContactNumber()
    {
        return $this->contact_number;
    }

    /**
     * Set contact_email
     *
     * @param string $contactEmail
     */
    public function setContactEmail($contactEmail)
    {
        $this->contact_email = $contactEmail;
    }

    /**
     * Get contact_email
     *
     * @return string 
     */
    public function getContactEmail()
    {
        return $this->contact_email;
    }

    /**
     * Set miscellaneous
     *
     * @param string $miscellaneous
     */
    public function setMiscellaneous($miscellaneous)
    {
        $this->miscellaneous = $miscellaneous;
    }

    /**
     * Get miscellaneous
     *
     * @return string 
     */
    public function getMiscellaneous()
    {
        return $this->miscellaneous;
    }

    /**
     * Set billing_address
     *
     * @param string $billingAddress
     */
    public function setBillingAddress($billingAddress)
    {
        $this->billing_address = $billingAddress;
    }

    /**
     * Get billing_address
     *
     * @return string 
     */
    public function getBillingAddress()
    {
        return $this->billing_address;
    }

    /**
     * Set mailing_address
     *
     * @param string $mailingAddress
     */
    public function setMailingAddress($mailingAddress)
    {
        $this->mailing_address = $mailingAddress;
    }

    /**
     * Get mailing_address
     *
     * @return string 
     */
    public function getMailingAddress()
    {
        return $this->mailing_address;
    }

    /**
     * Set accounts_active
     *
     * @param boolean $accountsActive
     */
    public function setAccountsActive($accountsActive)
    {
        $this->accounts_active = $accountsActive;
    }

    /**
     * Get accounts_active
     *
     * @return boolean 
     */
    public function getAccountsActive()
    {
        return $this->accounts_active;
    }

    /**
     * Set hosts_active
     *
     * @param boolean $hostsActive
     */
    public function setHostsActive($hostsActive)
    {
        $this->hosts_active = $hostsActive;
    }

    /**
     * Get hosts_active
     *
     * @return boolean 
     */
    public function getHostsActive()
    {
        return $this->hosts_active;
    }

    /**
     * Set enable_billing
     *
     * @param boolean $enableBilling
     */
    public function setEnableBilling($enableBilling)
    {
        $this->enable_billing = $enableBilling;
    }

    /**
     * Get enable_billing
     *
     * @return boolean 
     */
    public function getEnableBilling()
    {
        return $this->enable_billing;
    }

    /**
     * Add projects
     *
     * @param Monistix\OrganizationBundle\Entity\Project $projects
     */
    public function addProject(\Monistix\OrganizationBundle\Entity\Project $projects)
    {
        $this->projects[] = $projects;
    }
}