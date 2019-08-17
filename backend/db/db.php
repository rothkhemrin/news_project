<?php

    class Database{

        //private $cn=new mysqli('localhost','root','','news_sb'); ?

        public $cn;



        function connect(){

             $server_name="localhost";
             $user_name="root";
             $pwd="";
             $db_name="news_sb";

            $this->cn=new mysqli($server_name,$user_name,$pwd,$db_name);
            $this->cn->set_charset('utf8');

        }

        function insert($tbl,$val){

            $this->connect();

            $sql="insert into ".$tbl." values (".$val.")";

            if($this->cn->query($sql)){
                $this->last_id();
                return true;
            }
        }

        function update($tbl,$field,$condition){

            $this->connect();

            $sql="update ".$tbl." set ".$field." where ".$condition;

            $this->cn->query($sql);

        }

        function select($tbl,$field,$condition,$oder_field,$limit){

            $this->connect();

            $sql="select ".$field." from ".$tbl." where ".$condition." order by ".$oder_field." limit ".$limit;

            $result=$this->cn->query($sql);

            $num_rows=$result->num_rows;

            if ($num_rows==0){

                return 0;
            }

            else{

                $data=array();
                while($row=$result->fetch_array()){

                    $data[]=$row;
                }

                return $data;
            }
        }

        function max_id($id,$tbl){

            $this->connect();

            $sql="select max(".$id.") from ".$tbl;

            $result=$this->cn->query($sql);

            $num_rows=$result->num_rows;

            if ($num_rows==0){

                return 1;
            }
            else{

                $row=$result->fetch_array();

                $max_num=$row+1;

                return $max_num;
            }
        }

        function last_id(){

            return $this->cn->insert_id;
        }

        function duplicate_name($id,$tbl,$condition){

            $this->connect();
            $sql="select ".$id." from ".$tbl." where ".$condition;

            $result=$this->cn->query($sql);

            $num_rows=$this->$result->num_rows;

            if($num_rows==0){
                return true;
            }
            else{
                return false;
            }
        }
    }
