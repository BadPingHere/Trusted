<?php
echo "<script>console.log(`Hello! If you're seeing this, this is my special little console where i spend hours debugging! You shouldnt need to do anything here unless told by someone important, but you can always check the source code on my github if you want to poke around!`);</script>"; // Debug code
$asc = 0; // Fixes issues, so it's not empty
if ($_SERVER["REQUEST_METHOD"] == "POST") { //* Used as a flip-flop switch between ASC Chat
  if (empty($_POST['name'])) {
    $asc = 1;

  }
  else {
    if ($asc = 1) {
      $asc = 0;
    }
    else {
      $asc = 1;
    }
  }
}
if (!empty($asc)){
  echo "<script>console.log(`Asc: $asc`);</script>"; // Debug code
}
if ($asc == 1){
  $chatbox = 'agentchatbox';
}
else {
  $chatbox = 'chatbox';
}

ini_set('memory_limit', '512M');
ini_set('display_errors', '1');
function csv_content_parser($content)
{
    foreach (explode("\n", $content) as $line) {
        yield str_getcsv($line);
    }
}
function csvstring_to_array($string, $separatorChar = ',', $enclosureChar = '"', $newlineChar = "\n") {
  $array = array(); // idk who i took this from
  $size = strlen($string);
  $columnIndex = 0;
  $rowIndex = 0;
  $fieldValue="";
  $isEnclosured = false;
  for($i=0; $i<$size;$i++) {

      $char = $string[$i];
      $addChar = "";

      if($isEnclosured) {
          if($char==$enclosureChar) {

              if($i+1<$size && $string[$i+1]==$enclosureChar){
                  $addChar=$char;
                  $i++;
              }else{
                  $isEnclosured = false;
              }
          }else {
              $addChar=$char;
          }
      }else {
          if($char==$enclosureChar) {
              $isEnclosured = true;
          }else {

              if($char==$separatorChar) {

                  $array[$rowIndex][$columnIndex] = $fieldValue;
                  $fieldValue="";

                  $columnIndex++;
              }elseif($char==$newlineChar) {
                  echo $char; // this echo's like 1200 blank lines into the php web-side. this doesnt show on the html so i dont care.
                  $array[$rowIndex][$columnIndex] = $fieldValue;
                  $fieldValue="";
                  $columnIndex=0;
                  $rowIndex++;
              }else {
                  $addChar=$char;
              }
          }
      }
      if($addChar!=""){
          $fieldValue.=$addChar;

      }
  }

  if($fieldValue) { // save last field
      $array[$rowIndex][$columnIndex] = $fieldValue;
  }
  return $array;
}

$data1 = csvstring_to_array(file_get_contents("messages.csv")); // Im using 2 csv tbh but like idk man
$content2 = file_get_contents("opsummary.csv");$data2 = [];foreach (csv_content_parser($content2) as $fields) {array_push($data2, $fields);}
$content3 = file_get_contents("prechat.csv");$data3 = [];foreach (csv_content_parser($content3) as $fields) {array_push($data3, $fields);}
$content4 = file_get_contents("topology.csv");$data4 = [];foreach (csv_content_parser($content4) as $fields) {array_push($data4, $fields);}
$content5 = file_get_contents("users.csv");$data5 = [];foreach (csv_content_parser($content5) as $fields) {array_push($data5, $fields);}

$jsonText = file_get_contents('../json/classData-season6.json');
$classes = json_decode($jsonText, true);
$classes = array_map(function($obj) {return array_values($obj);},$classes);

$charges = json_decode(file_get_contents('../json/charges-season6.json'), true);

$adder = 1;
$helpmenumber = 1;
$mailchecker = 1;
$player = array("role");
$findernumber = 1;
$coverfind = array();
$deaths = array();
$skills = array(["role","skill","used_on","day"]);
$lifechangearray = array(["color","line","dayof","ifdied","ifmoled","ifarrested","ifimprovised","improviseddayof"]);
$sidebarnumber = 1;
$colornumber = 1;
$addman = 1;

$user = 1;
$admin = 0;
$daytime = 01;
function checkrole($number, $style_top)
{
  global $data2, $player, $data5, $user, $role, $admin, $coverfind, $daytime;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  $netsec_class = "Operation Leader | CCTV Specialist | Enforcer | Inside Man | Analyst | Network Specialist | Social Engineer | Blackhat | Improvised Hacker | Spearphisher | ";
  $nuet_class = "Bounty Hunter | Corrupt Detective | Double-crosser | Journalist | Loose Cannon | Script Kiddie | Panicked Blabbermouth | Resentful Criminal | Sociopath | Rival Hacker | ";
  if (empty($player[$number])){
    echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/blank.png">';
  } else {
    if (str_contains($agent_class, $player[$number][0])){
      if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {
        if ($data2[$number][0] == $coverfind[0][0] && $daytime < 40) { // Check if agent has cover
          echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/netsec.png">';
        }
        else {
          echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/agent.png">';
        }
      }
      else {
        if ($data5[$user][3]==$data5[$number][3]) {
          echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/agent.png">';
        }
        else {
          if (str_contains($agent_class, $role)){
            echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/agent.png">';
            }
            else {
              if ($admin == 1) {
                echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/agent.png">';
              } else {
                echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/blank.png">';
              }
            }
        }
      }
    } else {
      if(str_contains($netsec_class, $player[$number][0])){
        if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {
          echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/netsec.png">';
        }
        else {
          if ($data5[$user][3]==$data5[$number][3]) {
            echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/netsec.png">';
          }
          else {
            if ($admin == 1) {
              echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/netsec.png">';
            } else {
              echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/blank.png">';
            }
          }
        }
      } else {
        if(str_contains($nuet_class, $player[$number][0])){
          if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {
            echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/nuet.png">';
          }
          else {
            if ($data5[$user][3]==$data5[$number][3]) {
              echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/nuet.png">';
            }
            else {
              if ($admin == 1) {
                echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/nuet.png">';
              } else {
                echo '<img style="top:'.$style_top.';left:50px;" class="factionimg" src="/images/blank.png">';
              }
            }
          }
        }
      }
    }
  }
}
function checkheartbeat($number, $style_top)
{
  global $data2, $daytime, $player, $deaths;
  $alive = 'Alive';
  $dead = 'Dead';
  $arrested = 'Arrested';
  if (empty($data2[$number][3])){
    echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/blank.png">';
  } else {
    if(str_contains($alive, $data2[$number][3])){
      if ($player[$number][2] == 'before') {
        echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/alive.png">';
      }
      else {
        echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/alive.png">';
      }
    } else {
      if(str_contains($dead, $data2[$number][3])){
        if ($player[$number][2]  == 'before') {
          echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/alive.png">';
        }
        else {
          echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/dead.png">';
          $deaths[$data2[$number][0]] = "died"; // Used for votes, bodged together because i can woohoo!!!
        }
      } else {
        if(str_contains($arrested, $data2[$number][3])){
          if ($player[$number][2]  == 'before') {
            echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/alive.png">';
          }
          else {
            echo '<img style="top:'.$style_top.';" class="alivestatusimg" src="/images/arrested.png">';
            $deaths[$data2[$number][0]] = "arrested"; // Used for votes, bodged together because i can woohoo!!!
          }
        }
      }
    }
  }
}
function checkcolor($number)
{
  global $data2, $player, $admin, $user, $role;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  $netsec_class = "Operation Leader | CCTV Specialist | Enforcer | Inside Man | Analyst | Network Specialist | Social Engineer | Blackhat | Improvised Hacker | Spearphisher | ";
  $nuet_class = "Bounty Hunter | Corrupt Detective | Double-crosser | Journalist | Loose Cannon | Script Kiddie | Panicked Blabbermouth | Resentful Criminal | Sociopath | Rival Hacker | ";
  if (empty($data2[$number][3])){
    echo "blank";
  } else {
    if(str_contains($agent_class, $player[$number][0])){
      // Role is agent
      if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {  //check if they are alive or dead/arrested, anmd if its after its happened
        echo "841fa4"; // Dead Color
      }
      else {
          if($user == $number) {
            echo "846414"; // Agent Color
          }
          else {
              echo "e6e6e6"; // Unknown color (white)
          }
      }
    } else {
      if(str_contains($netsec_class, $player[$number][0])){
        // Role is Netsec
        if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {  //check if they are alive or dead/arrested, anmd if its after its happened
        echo "841fa4"; // Dead Color
        }
        else {
            if($user == $number) {
              echo "077d0c"; // Netsec Color
            }
            else {
              echo "e6e6e6"; // Unknown color (white)
            }
        }
      } else {
        if(str_contains($nuet_class, $player[$number][0])){
          // Role is neutral. Nuetral is hard to spell.
          if($player[$number][3] == 'Dead' || $player[$number][3] == 'Arrested' and $player[$number][2] == 'after') {  //check if they are alive or dead/arrested, anmd if its after its happened
          echo "841fa4"; // Dead Color
          }
          else {
              if($user == $number) {
                echo "4f0404"; // Neutral Color
              }
              else {
                echo "e6e6e6"; // Unknown color (white)
              }
          }
        }
      }
    }
  }
}
function checkcolornodeath($role) //* used for top right name
{
  global $data2;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  $netsec_class = "Operation Leader | CCTV Specialist | Enforcer | Inside Man | Analyst | Network Specialist | Social Engineer | Blackhat | Improvised Hacker | Spearphisher | ";
  $nuet_class = "Bounty Hunter | Corrupt Detective | Double-crosser | Journalist | Loose Cannon | Script Kiddie | Panicked Blabbermouth | Resentful Criminal | Sociopath | Rival Hacker | ";
  if (empty($role)){
    echo "blank";
  } else {
    if(str_contains($agent_class, $role)){
      // Role is agent
      echo "cca11d";
    } else {
      if(str_contains($netsec_class, $role)){
        // Role is Netsec
        echo "04d116";
      } else {
        if(str_contains($nuet_class, $role)){
          // Role is neutral. Nuetral is hard to spell.
          echo "ffffff";
        }
      }
    }
  }
}
function findday($param)
{
  global $lifechangearray, $adder, $data2, $daytime;
  if ($lifechangearray[$adder][0] == $data2[$param][0]){
    $keys = array_keys(array_column($lifechangearray, 0), $data2[$param][0]);
    //echo "<script>console.log('kegs: %O', ".json_encode($keys)." );</script>"; // Debug code
    if (count($keys) >= 2) { // Check for people with more than 2 logs. They are imp i thnk
      $impday = $lifechangearray[$keys[0]][7]; // Day of imping
      $otherday = $lifechangearray[$keys[1]][2]; // Day or arrest or whatever
      if (!empty($lifechangearray[$keys[1]][3])) {
        $pushrole = $lifechangearray[$keys[1]][3];
      }
      else {
        if (!empty($lifechangearray[$keys[1]][4])) {
          $pushrole = $lifechangearray[$keys[1]][4];
        }
        else {
          $pushrole = $lifechangearray[$keys[1]][5];
        }
      }
      if ($impday < $daytime) { // They are imp
        if ($otherday < $daytime) { // They are arrested/dead or sum
          $pushstring = [$data2[$param][2],$otherday,"after",$pushrole];
          global $player;
          array_push($player,$pushstring);
          $adder = 1;
        } else { // Not yet arrested/dead
          $pushstring = [$data2[$param][2],$otherday,"before",$pushrole];
          global $player;
          array_push($player,$pushstring);
          $adder = 1;
        }
      }
      else { // They are not imp, nor arrested/murdered/or whatever
        $pushstring = [$data2[$param][2],$impday,"before",$lifechangearray[$keys[0]][6]];
        global $player;
        array_push($player,$pushstring);
        $adder = 1;
      }
    }
    else {
      $day = $lifechangearray[$adder][2]; // It for some reason removes the _, so its 21 rather than 2_1, which is genuinely a blessing
      //echo "<script>console.log(`".$lifechangearray[$adder][0]."`);</script>"; // Debug code
      //echo "<script>console.log(".$day.");</script>"; // Debug code
        if ($day >= $daytime) {
          $pushstring = [$data2[$param][1],$day,"before",$data2[$param][3]];
          global $player;
          array_push($player,$pushstring);
          $adder = 1;
        }
        else {
          $pushstring = [$data2[$param][2],$day,"after",$data2[$param][3]];
          global $player;
          array_push($player,$pushstring);
          $adder = 1;
        }
    }
  }
  else {
    $adder++;
    findday($param);
  }
}
function findrole($param) // todo: Check for frames. I check for al cover, but no one in my test game used frame so i dont wanna check if if i cant debug
{
  global $data2, $role, $lifechangearray;

  if (empty($param)) {
    return;
  }
  else {
    if (empty($data2[$param][1])){
      return; 
    } else {// Checks if user has been moled, arrested, or murdered.
      foreach ($lifechangearray as $sub_array) {
        if (@$sub_array[0] === $data2[$param][0]) {
          findday($param);
          return true;
        }
      }
      global $player;
      $pushstring = [$data2[$param][1],[],[],$data2[$param][3]];
      array_push($player,$pushstring);
      return false;
    } 
  }
}
function roleimage($classname)
{
  if (empty($classname)){
    echo "blank";
  }
  else {
    echo $classname;
  }
}
function printsidebar($sidebarnumber) //* made this so my html part of the code looks better.
{
  global $data5, $user;
  if(empty($data5[$sidebarnumber][3])) {

  }else {
    if($data5[$user][3]==$data5[$sidebarnumber][3]){
      $output = $data5[$sidebarnumber][3] . " (You)";
      echo $output;
    }else{
      echo $data5[$sidebarnumber][3];
    }
  }
}
function findeaths() //* Checks for changes to roles (moles, ih, maybe cover/frame), and cementation of roles (arrest/death/nothing)
{
  global $data1, $findernumber, $matches, $lifechangearray;
  $color = "";
  $linenumber = "";
  $dayof = "";
  $died = "";
  $moled = "";
  $arrested = "";
  $ih = "";
  $ihdayof = "";
  $mole_message = "In order to avoid prison, you have accepted a plea deal from AGENTs. You are now working for them";
  if (empty($data1[$findernumber][9])) {
    echo "<script>console.log('Life Change Array: %O', ".json_encode($lifechangearray)." );</script>"; // Debug code
  }
  else {
    if (preg_match('/style="color:#fff;text-align:center;">[A-Za-z0-9]+\\.[A-Za-z0-9]+ was found dead under suspicious circumstances\\./i',$data1[$findernumber][9])) {  // Checks if died
      preg_match('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i',$data1[$findernumber][9], $matches, PREG_UNMATCHED_AS_NULL);
      $color = implode(" ", $matches);
      $linenumber = $findernumber;
      $dayof = $data1[$findernumber][2];
      $died = "Died";
    }
    if (str_contains($data1[$findernumber][9], $mole_message)) {  // Checks if moled
      preg_match('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i',$data1[$findernumber][9], $matches, PREG_UNMATCHED_AS_NULL);
      $color = implode(" ", $matches);
      $linenumber = $findernumber;
      $dayof = $data1[$findernumber][2];
      $moled = "Moled";
    }
    if (preg_match('/style="color:#fff;text-align:center;">[A-Za-z]+\\.[A-Za-z]+ was arrested last night\\./i',$data1[$findernumber][9])) {  // Checks if arrested
      preg_match('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i',$data1[$findernumber][9], $matches, PREG_UNMATCHED_AS_NULL);
      $color = implode(" ", $matches);
      $linenumber = $findernumber;
      $dayof = $data1[$findernumber][2];
      $arrested = "Arrested";
    }
    if (preg_match('/You have followed the Operation Leader\'s emergency protocols/i',$data1[$findernumber][9])) {  // Checks if ih
      preg_match('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i',$data1[$findernumber][9], $matches, PREG_UNMATCHED_AS_NULL);
      $color = implode(" ", $matches);
      $linenumber = $findernumber;
      $dayof = $data1[$findernumber][2];
      $ih = "Improvised";
      $ihdayof = $data1[$findernumber][2];
    }
    if(empty($color)) {
      $findernumber++;
      findeaths();
    }
    else {
      $push_array = [$color,$linenumber,$dayof,$died,$moled,$arrested,$ih,$ihdayof];
      array_push($lifechangearray,$push_array);
      $findernumber++;
      findeaths();
    }
  }
}
function classimages($agentnumber, $style_top)
{
  global $player, $user, $admin, $coverfind, $daytime, $data2;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  $netsec_class = "Operation Leader | CCTV Specialist | Enforcer | Inside Man | Analyst | Network Specialist | Social Engineer | Blackhat | Improvised Hacker | Spearphisher | ";
  $nuet_class = "Bounty Hunter | Corrupt Detective | Double-crosser | Journalist | Loose Cannon | Script Kiddie | Panicked Blabbermouth | Resentful Criminal | Sociopath | Rival Hacker | ";
  if (empty($player[$agentnumber][0])) {
    echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/blank.png">';
    return;
  }
  if ($player[$agentnumber][3] == 'Dead' || $player[$agentnumber][3] == 'Arrested' and $player[$agentnumber][2] == 'after') { // User, dead, always gets image
    if ($data2[$agentnumber][0] == $coverfind[0][0] && $daytime < 40) {
      echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/'.$coverfind[0][1].'.png">';
    }
    else {
      echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/'.$player[$agentnumber][0].'.png">';
    }
  }
  else {
    if (str_contains($agent_class, $player[$agentnumber][0]) && str_contains($agent_class, $player[$user][0])){ // Check if current user is agent 
      echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/'.$player[$agentnumber][0].'.png">';
    }
    else {
      if ($admin == 1) {
        echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/'.$player[$agentnumber][0].'.png">';
      }
      else {
        echo '<img style="top:'.$style_top.';left:398px;" class="agentimg" src="/images/classes/blank.png">';
      }
    }
  }
}
function findcover()
{
  global $data1, $addman, $matches, $coverfind;
  $color = "";
  $role = "";
  if (!empty($coverfind)) {
    echo "<script>console.log('Cover: %O', ".json_encode($coverfind)." );</script>"; // Debug code
  }
  else {
    if (preg_match('/have a cover as \'[^\']*\' in the event of an early /i',$data1[$addman][9])) {  // Checks if died
      preg_match('/\'[^\']*\'/i' ,$data1[$addman][9], $matches1,);
      $role_before = implode("", $matches1);
      $role = trim($role_before,"'"); // remove the ' characters
      preg_match('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$addman][9], $matches2,);
      $color = implode(" ", $matches2);
    }
    if(empty($color)) {
      $addman++;
      findcover();
    }
    else {
      $push_array = [$color,$role];
      array_push($coverfind,$push_array);
      $addman++;
      findcover();
    }
  }
}
function messages() // TODO: doesnt show the stupid fucking messages where it shows you tried to like hack or ddos, yknow, here: https://cdn.upload.systems/uploads/gIkMUSyd.png
{
  global $data1, $helpmenumber, $daytime, $player, $user, $data2, $asc, $end, $lastday;
  if (empty($data1[$helpmenumber][9])){
    //done
  }
  else {
    if ($asc == 1){ //* Should be impossible to reach if you arent agent
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][3] == 1 ) { //* ASC Chat
        echo "<div>";
        preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches);
        echo '<img class="avatarimg" src="/avatars/'.$matches[0][0].'">';
        $param = '<tr> <td style="text-align:left;width:25%;">   <img src="../../avatars/'.$matches[0][0].'" style="width:48px;height:48px;"/> '.$matches[0][1].': </td> <td style="text-align:justify;width:75%;color: #ffc91b;;">';
        $message_1 = str_replace($param,'',$data1[$helpmenumber][9]);
        if (str_contains(str_replace('</td></tr>','',$message_1),'[!]')) { //! Needs Fix: Multiple Pings, as in [!][!], are not accounted for
          $message = substr(str_replace('</td></tr>','',$message_1), 3);
          echo '<div class="chatusername">'.$matches[0][1].':&emsp;<div class="chatmessagehighlighted"><span style="color:#FFFF00;">[!]</span>'.$message.'</div></div>';
        }
        else {
          $message = str_replace('</td></tr>','',$message_1);
          echo '<div class="chatusername  ">'.$matches[0][1].':&emsp;<div class="chatmessage">'.$message.'</div></div>';
        }
        echo "</div>";
      }
    }else {
      if (empty($data1[$helpmenumber][0]) && $data1[$helpmenumber][0] <= $daytime) { //* Day Change messages | has to be manual, so its like 150~ lines
        { // Messages
          $endline = '<tr><td colspan="2" style="color:#fff;text-left;">No actions were committed this turn.</td></tr>';
          $prepnight = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Preparation Night Chat Log «</td></tr>';
          $day1 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 1 Chat Log «</td></tr>';
          $night1 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 1 Chat Log «</td></tr>';
          $day2 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 2 Chat Log «</td></tr>';
          $night2 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 2 Chat Log «</td></tr>';
          $day3 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 3 Chat Log «</td></tr>';
          $night3 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 3 Chat Log «</td></tr>';
          $day4 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 4 Chat Log «</td></tr>';
          $night4 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 4 Chat Log «</td></tr>';
          $day5 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 5 Chat Log «</td></tr>';
          $night5 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 5 Chat Log «</td></tr>';
          $day6 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 6 Chat Log «</td></tr>';
          $night6 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 6 Chat Log «</td></tr>';
          $day7 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 7 Chat Log «</td></tr>';
          $night7 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 7 Chat Log «</td></tr>';
          $day8 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 8 Chat Log «</td></tr>';
          $night8 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 8 Chat Log «</td></tr>';
          $day9 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 9 Chat Log «</td></tr>';
          $night9 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 9 Chat Log «</td></tr>';
          $day10 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Day 10 Chat Log «</td></tr>';
          $night10 = '<tr><td colspan="2" style="color:#00ff01;text-align:right;font-size:1.5em;">Night 10 Chat Log «</td></tr>';
        }
        $param = $helpmenumber+1;
        if ($data1[$helpmenumber][10] == 01 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> PREPARATION NIGHT</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 10 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 1</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 11 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 1</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 20 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 2</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 21 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 2</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 30 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 3</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 31 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 3</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 40 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 4</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 41 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 4</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 50 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 5</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 51 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 5</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 60 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 6</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 61 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 6</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 70 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 7</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 71 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 7</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 80 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 8</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 81 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 8</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 90 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 9</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 91 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 9</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 100 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> DAY 10</div>';
          echo "</div>";
        }
        if ($data1[$helpmenumber][10] == 101 && $data1[$param][0] < $daytime && $data1[$param][9] !== $endline) {
          echo "<div>";
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          echo '<div class="chatusername" style="color:#04ca15">>>>> Night 10</div>';
          echo "</div>";
        }
      }
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][4] == 1 ) { //* Dead Chat
        if ($player[$user][2] = "After" && $player[$user][3] = "Dead") {
          echo "<div>";
          preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches);
          echo '<img class="avatarimg" src="/avatars/'.$matches[0][0].'">';
          $param = '<tr> <td style="text-align:left;width:25%;">   <img src="../../avatars/'.$matches[0][0].'" style="width:48px;height:48px;"/> '.$matches[0][1].': </td> <td style="text-align:justify;width:75%;color: #911eb4;;">';
          $message_1 = str_replace($param,'',$data1[$helpmenumber][9]);
          if (str_contains(str_replace('</td></tr>','',$message_1),'[!]')) { //! Needs Fix: Multiple Pings, as in [!][!], are not accounted for
            $message = substr(str_replace('</td></tr>','',$message_1), 3);
            echo '<div class="chatusernamedead">'.$matches[0][1].':&emsp;<div class="chatmessagehighlighted"><span style="color:#FFFF00;">[!]</span>'.$message.'</div></div>';
          }
          else {
            $message = str_replace('</td></tr>','',$message_1);
            echo '<div class="chatusernamedead">'.$matches[0][1].':&emsp;<div class="chatmessage">'.$message.'</div></div>';
          }
          echo "</div>";
        }
      }
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][5] == 1 ) { //* Alive Chat
        echo "<div>";
        preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches);
        echo '<img class="avatarimg" src="/avatars/'.$matches[0][0].'">';
        $param = '<tr> <td style="text-align:left;width:25%;">   <img src="../../avatars/'.$matches[0][0].'" style="width:48px;height:48px;"/> '.$matches[0][1].': </td> <td style="text-align:justify;width:75%;color: #fff;;">';
        $message_1 = str_replace($param,'',$data1[$helpmenumber][9]);
        if (str_contains(str_replace('</td></tr>','',$message_1),'[!]')) { //! Needs Fix: Multiple Pings, as in [!][!], are not accounted for
          $message = substr(str_replace('</td></tr>','',$message_1), 3);
          echo '<div class="chatusername">'.$matches[0][1].':&emsp;<div class="chatmessagehighlighted"><span style="color:#FFFF00;">[!]</span>'.$message.'</div></div>';
        }
        else {
          $message = str_replace('</td></tr>','',$message_1);
          echo '<div class="chatusername">'.$matches[0][1].':&emsp;<div class="chatmessage">'.$message.'</div></div>';
        }
        echo "</div>";
        //echo "<script>console.log('matrches: %O', ".json_encode($matches)." );</script>"; // Debug code
      }
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][6] == 1 ) { //* Broadcast 
          echo "<div>";
          preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches);
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          $message_1 = str_replace('<tr><td colspan="2"><pre><b>ANONYMOUS BROADCAST:</b>','',$data1[$helpmenumber][9]);
          $message = str_replace('</pre></td></tr>','',$message_1);
          echo '<div class="chatusername" style="color:#04ca15">New mail from undisclosed sender:&emsp;<div class="chatmessage" style="color:#04ca15">[BROADCAST]'.$message_1.'</div></div>';
          echo "</div>";
          //echo "<script>console.log('matrches: %O', ".json_encode($matches)." );</script>"; // Debug code
      }
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][7] == 1 ) { //* Mail 
          preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches2);
          if ($matches2[0][3] == $data2[$user][0])  { // Checks if its being sent TO the current user
            preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches2);
            echo "<div>";
            echo '<img class="avatarimg" src="/avatars/00000.png">';
            $text = '<tr><td><table><tbody><tr><td style="text-center;margin:auto;">   <img src="../../avatars/'.$matches2[0][0].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][1].' </td><td style="vertical-align:middle;">» » »</td> <td style="text-align:center;margin:auto;">   <img src="../../avatars/'.$matches2[0][2].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][3].' </td></tr></tbody></table></td><td><pre><b>Private message:</b>';
            $broadcast_1 = str_replace($text, '', $data1[$helpmenumber][9]);
            $broadcast_2 = str_replace('</pre></td></tr>', '', $broadcast_1);
            $result = explode('<br/>',$broadcast_2); // Future refrence : This line removes everything after the br tag, only displaying the title of the mail, and not body.
            echo '<div class="chatusername" style="color:#04ca15">New mail from '.$matches2[0][1].':&emsp;<div class="chatmessage" style="color:#04ca15">'.$result[0].'</div></div>';
            echo "</div>";
            //echo "<script>console.log('matrches: %O', ".json_encode($matches)." );</script>"; // Debug code
          }
          if ($matches2[0][1] == $data2[$user][0])  { // Checks if its being sent FROM the current user
            preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches2);
            echo "<div>";
            echo '<img class="avatarimg" src="/avatars/00000.png">';
            $text = '<tr><td><table><tbody><tr><td style="text-center;margin:auto;">   <img src="../../avatars/'.$matches2[0][0].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][1].' </td><td style="vertical-align:middle;">» » »</td> <td style="text-align:center;margin:auto;">   <img src="../../avatars/'.$matches2[0][2].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][3].' </td></tr></tbody></table></td><td><pre><b>Private message:</b>';
            $broadcast_1 = str_replace($text, '', $data1[$helpmenumber][9]);
            $broadcast_2 = str_replace('</pre></td></tr>', '', $broadcast_1);
            $result = explode('<br/>',$broadcast_2); // Future refrence : This line removes everything after the br tag, only displaying the title of the mail, and not body.
            echo '<div class="chatusername" style="color:#04ca15">The email \''.$result[0].'\' has been sent sucessfully to '.$matches2[0][3].'</div>';
            echo "</div>";
            //echo "<script>console.log('matrches: %O', ".json_encode($matches)." );</script>"; // Debug code
          }
      }
      if ($data1[$helpmenumber][0] <= $daytime && $data1[$helpmenumber][8] == 1 ) { //* Votes 
          echo "<div>";
          preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$helpmenumber][9], $matches);
          echo '<img class="avatarimg" src="/avatars/00000.png">';
          $message_1 = str_replace('<tr><td colspan="2" style="color:#ff0001;text-align:center;font-size:1.0em;">','',$data1[$helpmenumber][9]);
          $message = str_replace('</td></tr>','',$message_1);
          echo '<div class="chatusername" style="color:#04ca15">'.$message.'</div>';
          echo "</div>";
          //echo "<script>console.log('matrches: %O', ".json_encode($matches)." );</script>"; // Debug code
      }
    }
    $helpmenumber++;
    messages();
  }
}
function mail2() // TODO: Scrollbar, onclick show mail
{
  global $data1, $daytime, $mailchecker, $data2, $user;

  $i1 = count($data1);
  while ($i1 > 0) { // Scrolls through until 0
    if (empty($data1[$i1][9]) && $mailchecker == 1){
      $i1 --;
    }
    if (empty($data1[$i1][9]) && $mailchecker == 0){
      //done
    }
    else {
      if ($data1[$i1][0] <= $daytime && $data1[$i1][6] == 1 ) { // echo broadcast
          //echo "<script>console.log(2);</script>"; // Debug code 
          echo  '<div class="mailholderinner">';
          echo '<img style="width:36px;height:28px;float:left;" src="/images/mail.png">';
          $broadcast_1 = str_replace('<tr><td colspan="2"><pre><b>ANONYMOUS BROADCAST:</b> ', '', $data1[$i1][9]);
          echo '<div class="mailmessage">Undisclosed&emsp;&emsp;<div class="mailmessage2">[BROADCAST] '.str_replace('</pre></td></tr>', '', $broadcast_1).'</div></div>';;
          echo '</div>';
          $mailchecker = 0;
        }
      if ($data1[$i1][0] <= $daytime && $data1[$i1][7] == 1 ) { // Echo mail
        preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i' ,$data1[$i1][9], $matches2,);
        if ($matches2[0][3] == $data2[$user][0])  {
          echo  '<div class="mailholderinner">';
          echo '<img style="width:36px;height:28px;float:left;" src="/images/mail.png">';
          $text = '<tr><td><table><tbody><tr><td style="text-center;margin:auto;">   <img src="../../avatars/'.$matches2[0][0].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][1].' </td><td style="vertical-align:middle;">» » »</td> <td style="text-align:center;margin:auto;">   <img src="../../avatars/'.$matches2[0][2].'" style="width:48px;height:48px;"/><br/> '.$matches2[0][3].' </td></tr></tbody></table></td><td><pre><b>Private message:</b>';
          $broadcast_1 = str_replace($text, '', $data1[$i1][9]);
          $broadcast_2 = str_replace('</pre></td></tr>', '', $broadcast_1);
          $result = explode('<br/>',$broadcast_2); // Future refrence : This line removes everything after the br tag, only displaying the title of the mail, and not body.
          echo '<div class="mailmessage">'.$matches2[0][1].'&emsp;&emsp;<div class="mailmessage2">'.$result[0].'</div></div>';;
          echo '</div>';
          $mailchecker = 0;
        }
      }
    }
    $i1--;
  }
  if ($i1 == 0 && $mailchecker == 1) { // Checks if there is no mail
    echo '<div class="mailholderinner">';
    echo '<div class="mailempty">No emails yet.</div>';
    echo '</div>';
    return('done');
  }
}
function checkforooc($role, $time)
{
  global $classes, $player, $user, $day, $data1, $data2, $skills, $charges;

  $i = 0;
  while ($i < count($data1)){ //* We should theoretically put *every* ooc message, but i dont have that.
    if ($data1[$i][2] == $time && str_contains($data1[$i][9],'('.$role.') You were occupied last night and failed to complete your task.')) {
      return true;
    }
    $i++;
  }
}
function capabilities() // TODO: Make it work with skills that give a random skill; ex. AL; check for skills that add to other skills, like create hideout.
{
  global $daytime, $role, $classes, $player, $user, $day, $data1, $data2, $skills, $charges;
  if ($daytime == 01) {
    echo '<div class="prepcapabilities">Tonight\'s the night we meet.<br>The hac​k begins tomorrow.</div>';
  }
  else {
    // Find out what role the player is via the role variable and comparing it with the classes array.
    $i = 0;
    while ($i < 16) {
      if ($classes[$i][2] == $role) {
        $i2 = 0;
        while ($i2 < count($data1)) {
          $html_param = 'used skill <a href="https://www.playuntrusted.com/manual/skills/#';
          if (strpos($data1[$i2][9], ''.$data2[$user][0].':') == true && $data1[$i2][1] < $daytime && strpos($data1[$i2][9],$html_param) == true) { // Before today 
            if (strpos($data1[$i2][9], '</a> on') == true) { // Checks if the skill was used on someone/something
              $text = str_replace(''.$data2[$user][0].':  '.$data2[$user][0].' used skill', '', trim(strip_tags($data1[$i2][9])));
              //$used_on = str_replace(' on', '',substr($text, strpos($text, ' on')));
              $findit = explode(' on ', $text);
              $used_on = $findit[1];
              $used = trim($findit[0]); // We use trim because of a lone space at the start of the string.
              if (checkforooc($data2[$user][0], $data1[$i2][1]) == false){
                array_push($skills, [$data2[$user][0], $used, $used_on, $data1[$i2][1]]);
              }
              //echo "<script>console.log(`Used: ".$used.", Used on: ".$used_on."`);</script>"; // Debug code

            }
            else { // Used on self
              $text = str_replace(''.$data2[$user][0].':  '.$data2[$user][0].' used skill', '', trim(strip_tags($data1[$i2][9])));
              $used = trim($text);
              if (checkforooc($data2[$user][0], $data1[$i2][1]) == false){
                array_push($skills, [$data2[$user][0], $used,'', $data1[$i2][1]]);
              }
              //echo "<script>console.log(`Used: ".$used."`);</script>"; // Debug code
            }
          }
          if (strpos($data1[$i2][9], ''.$data2[$user][0].':') == true && $data1[$i2][1] == $daytime && strpos($data1[$i2][9],$html_param) == true) { // Today
            if (strpos($data1[$i2][9], '</a> on') == true) { // Checks if the skill was used on someone/something
              $text = str_replace(''.$data2[$user][0].':  '.$data2[$user][0].' used skill', '', trim(strip_tags($data1[$i2][9])));
              //$used_on = str_replace(' on', '',substr($text, strpos($text, ' on')));
              $findit = explode(' on ', $text);
              $used_on = $findit[1];
              $used = trim($findit[0]); // We use trim because of a lone space at the start of the string.
              if (checkforooc($data2[$user][0], $data1[$i2][1]) == false){
                array_push($skills, [$data2[$user][0], $used, $used_on, $data1[$i2][1]]);
              }
              //echo "<script>console.log(`Used-T: ".$used.", Used on: ".$used_on."`);</script>"; // Debug code

            }
            else { // Used on self
              $text = str_replace(''.$data2[$user][0].':  '.$data2[$user][0].' used skill', '', trim(strip_tags($data1[$i2][9])));
              $used = trim($text);
              if (checkforooc($data2[$user][0], $data1[$i2][1]) == false){
                array_push($skills, [$data2[$user][0], $used,'', $data1[$i2][1]]);
              }
              //echo "<script>console.log(`Used-T: ".$used."`);</script>"; // Debug code
            }
          }
          $i2++;
        }
        echo "<script>console.log('Skills: %O', ".json_encode($skills)." );</script>"; // Debug code
        echo "<script>console.log('Charges Object: %O', ".json_encode($charges)." );</script>"; // Debug code
        if (substr($daytime, -1) == 0) { // Checks if it's daytime
          $switch = 9; // Use this for the day-time skills, allows us to copy and paste the below code when we need to make changes
          for ($i3 = 0; $i3 <= 4; $i3++){
            if (!empty($classes[$i][$switch][$i3])) {
              $charges_param = $charges[$role][$classes[$i][$switch][$i3]]['charges'];
              $cd = $charges[$role][$classes[$i][$switch][$i3]]['cd'];
              //look in $skills array for the skill and see how many times its been used
              $i4 = 0;
              $skills_param = 0;
              $time_since_use = 'unset';
              while ($i4 < count($skills)) {
                if ($skills[$i4][1] == $classes[$i][$switch][$i3] && $skills[$i4][3] < $daytime) { // process to remove charges from skills that have been used
                  $skills_param++;
                  $time_since_use = $daytime-$skills[$i4][3];
                }
                $i4++;
              }
              // If the above function has been used, then echo we enter
              if ($charges_param == 999999){
                echo '<div class="capaholderinner">';
                echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges"><img style="margin-top:18px;float:right;" src="/images/infinity.png"></div></div>';
                echo '</div>';
              }
              else {
                if ($skills_param >= 0) {
                  if ($charges_param-$skills_param === 0) { // Optimacy lower for unusable skills
                    echo '<div class="capaholderinner" style="opacity: 0.3;">';
                    echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                    echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                    echo '</div>';
                  }
                  else {
                    if (!$time_since_use == 'unset'|| $time_since_use < $cd){ // If they are still on cooldown, make it unsuable
                      echo '<div class="capaholderinner" style="opacity: 0.3;">';
                      echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                      echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                      echo '</div>';
                    } 
                    else {
                      echo '<div class="capaholderinner">';
                      echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                      echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                      echo '</div>';
                    }
                  }
                }
                else {
                  echo '<div class="capaholderinner">';
                  echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                  echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param.'x</div></div>';
                  echo '</div>';
                }
              }
            }
          }
        }
        else { // Its night-time
          $switch = 10; // Use this for the night-time skills, allows us to copy and paste the above code when we need to make changes
          for ($i3 = 0; $i3 <= 4; $i3++){
            if (!empty($classes[$i][$switch][$i3])) {
              $charges_param = $charges[$role][$classes[$i][$switch][$i3]]['charges'];
              $cd = $charges[$role][$classes[$i][$switch][$i3]]['cd'];
              //look in $skills array for the skill and see how many times its been used
              $i4 = 0;
              $skills_param = 0;
              $time_since_use = 'unset';
              while ($i4 < count($skills)) {
                if ($skills[$i4][1] == $classes[$i][$switch][$i3] && $skills[$i4][3] < $daytime) { // process to remove charges from skills that have been used
                  $skills_param++;
                  $time_since_use = $daytime-$skills[$i4][3];
                }
                $i4++;
              }
              // If the above function has been used, then echo we enter
              if ($charges_param == 999999){
                echo '<div class="capaholderinner">';
                echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges"><img style="margin-top:18px;float:right;" src="/images/infinity.png"></div></div>';
                echo '</div>';
              }
              else {
                if ($skills_param >= 0) {
                  if ($charges_param-$skills_param === 0) { // Optimacy lower for unusable skills
                    echo '<div class="capaholderinner" style="opacity: 0.3;">';
                    echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                    echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                    echo '</div>';
                  }
                  else {
                    if (!$time_since_use == 'unset'|| $time_since_use < $cd){ // If they are still on cooldown, make it unsuable
                      echo '<div class="capaholderinner" style="opacity: 0.3;">';
                      echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                      echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                      echo '</div>';
                    } 
                    else {
                      echo '<div class="capaholderinner">';
                      echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                      echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param-$skills_param.'x</div></div>';
                      echo '</div>';
                    }
                  }
                }
                else {
                  echo '<div class="capaholderinner">';
                  echo '<img style="width:50px;height:50px;float:left;" src="/images/skills/'.$classes[$i][$switch][$i3].'.png">';
                  echo '<div class="capaskill">'.$classes[$i][$switch][$i3].'<div class="capacharges">'.$charges_param.'x</div></div>';
                  echo '</div>';
                }
              }
            }
          }
        }
      }
      $i++;
    }
  }
}
function capaselected() 
{
  global $skills, $daytime, $classes, $role;
  $style=array("110px","165px","224px","285px");
  $i = 1;
  while ($i < count($skills)) {
    if ($skills[$i][3] == $daytime) {
      // Scroll through the classes array and find the skill.
      $i2 = 0;
      while ($i2 < count($classes)) {
        if ($classes[$i2][2] == $role) {
          $i3 = 0;
          // Check if $daytime ends in 1 or 0
          if (substr($daytime, -1) == 1) {
            while ($i3 < count($classes[$i2][10])) { // Night-time
              if ($classes[$i2][10][$i3] == $skills[$i][1]) {
                echo '<img class="capaselectedimg" src="/images/selected.png" style="top: '.$style[$i3].';left: 480px;">';
              }
              $i3++;
            }
          }
          else { // Day-time
            while ($i3 < count($classes[$i2][9])) {
              if ($classes[$i2][9][$i3] == $skills[$i][1]) {
                echo '<img class="capaselectedimg" src="/images/selected.png" style="top: '.$style[$i3].';left: 480px;">';
              }
              $i3++;
            }
          }
        }
        $i2++;
      }
    }
    $i++;
  }
}
function timebox()
{
  global $daytime;
  
  if ($daytime == 01) {
    echo '<div class="timeboxday">PREPERATION NIGHT</div>';
  }
  else {
    if (!substr($daytime, -1) == 1) { // Its day-time
      echo '<div class="timeboxday">DAY '.substr($daytime,0,1).'</div>';
    }
    else { // Its night-time
      echo '<div class="timeboxday">NIGHT '.substr($daytime,0,1).'</div>';
    }
  }
}
function votes() //* Adds the votes to the user tab thingy. Not integreated into printsidebar() becuase im working on this a month later
{
  global $user, $daytime, $player, $data1, $data2, $deaths;
  
  echo "<script>console.log('deaths: %O', ".json_encode($deaths)." );</script>"; // Debug code
  // Log all votes into an array here
  $i = 1;
  $votes = array();
  while ($i < count($data1)) {
    if ($data1[$i][8] == 1 && $data1[$i][0] == $daytime) {
      preg_match_all('/[A-Za-z0-9]+\\.[A-Za-z0-9]+/i',$data1[$i][9], $matches, PREG_UNMATCHED_AS_NULL);
      array_push($votes, [$matches[0][1],$matches[0][2]]);
    }
    $i++;
  }
  $ol_index = -1; // Find ol using this. this shouldnt be this hard
  for ($i = 1; $i < count($data2); $i++) {
    if ($data2[$i][1] == 'Operation Leader') {
      $ol_index = $i;
      break;
    }
  }
  // Turn that array into a number and dot here.
  $i2 = 0;
  $ol_voted = false;
  $style = array("","250px","306px","365px","418px","480px","540px","595px","655px","710px","770px","825px","885px","940px","1000px","1055px","1115px");
  $voted = array();
  while ($i2 < count($votes)) {
    $i3 = 1;
    while ($i3 < count($data2)) {
      if ($data2[$i3][0] == $votes[$i2][0]) { // Checks if the user voted
        echo '<span style="position:absolute;top:'.$style[$i3].';left:85px;" class="votedot"></span>';
      }
      if ($data2[$i3][0] == $votes[$i2][1]) { // Checks if the user got voted
        $user_in_question = $data2[$i3][0];
        if (!isset($voted[$user_in_question])) { // This adds the vote to the array
          $voted[$user_in_question] = 1;
        } else {
          $voted[$user_in_question]++;
        }
        if ($votes[$i2][0] == $data2[$ol_index][0]){ // Checks if user is OL to add to counter
          $ol_voted = $user_in_question;
          $voted[$user_in_question]++;
        }
      }
      $i3++;
    }
    $i2++;
  }
  for ($i = 1; $i < count($data2); $i++) {
    $player_name = $data2[$i][0];
    if (isset($voted[$player_name])){ // If set, we get the votes
      $vote_count = $voted[$player_name];
    }
    else {
      $vote_count = false;
    }
    if (!$vote_count == false){
      if ($ol_voted == $player_name) {
        $hidden_vote = $vote_count-1;
        $param1 = count($player)-1;
        $param2 = count($deaths);
        if ($hidden_vote / ($param1 - $param2) > 0.5) { // Check if more than 50 percent of the lobby voted for the player
          echo '<div class="votenumber" style="top: '.$style[$i].';left: 390px;">'.$hidden_vote.'</div>';
        }
        else {
          echo '<div class="votenumber" style="top: '.$style[$i].';left: 390px;color:red">'.$hidden_vote.'</div>';
        }
      }
      else {
        $param1 = count($player)-1;
        $param2 = count($deaths);
        if ($vote_count / ($param1 - $param2) > 0.5) { // Check if more than 50 percent of the lobby voted for the player
          echo '<div class="votenumber" style="top: '.$style[$i].';left: 390px;">'.$vote_count.'</div>';
        }
        else {
          echo '<div class="votenumber" style="top: '.$style[$i].';left: 390px;color:red">'.$vote_count.'</div>';
        }
      }
    }
  }
  echo "<script>console.log('Votes: %O', ".json_encode($votes)." );</script>"; // Debug code
  echo "<script>console.log('Voted: %O', ".json_encode($voted)." );</script>"; // Debug code
}
function music()
{
  global $role;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  $netsec_class = "Operation Leader | CCTV Specialist | Enforcer | Inside Man | Analyst | Network Specialist | Social Engineer | Blackhat | Improvised Hacker | Spearphisher | ";
  $nuet_class = "Bounty Hunter | Corrupt Detective | Double-crosser | Journalist | Loose Cannon | Script Kiddie | Panicked Blabbermouth | Resentful Criminal | Sociopath | Rival Hacker | ";
  if (str_contains($agent_class, $role)){
    echo 'agent';
  }
  if (str_contains($netsec_class, $role)){
    echo 'netsec';
  }
  if (str_contains($nuet_class, $role)){
    echo 'nuetral';
  }
}
function agentbutton()
{
  global $role;
  $agent_class = "Agent Leader | Field Agent | Forensics Specialist | Mole (Converted Field Ops) | Mole (Converted Inv.) | Mole (Converted Offensive) | Runaway Snitch |";
  if (str_contains($agent_class, $role)){
    echo '<button>change to asc</button>';
  }
}

findcover();
findeaths();

$i = 1;
$times_to_run = 17;
while ($i < $times_to_run)
{
  findrole($i);
  $i++;
}
$role = $player[$user][0];
echo "<script>console.log('Data1: %O', ".json_encode($data1)." );</script>"; // Debug code
echo "<script>console.log('Data2: %O', ".json_encode($data2)." );</script>"; // Debug code
echo "<script>console.log('Player: %O', ".json_encode($player)." );</script>"; // Debug code
//echo "<script>console.log('Data3: %O', ".json_encode($data3)." );</script>"; // Debug code
//echo "<script>console.log('Data4: %O', ".json_encode($data4)." );</script>"; // Debug code
//echo "<script>console.log('Data5: %O', ".json_encode($data5)." );</script>"; // Debug code
echo "<script>console.log('Classes: %O', ".json_encode($classes)." );</script>"; // Debug code

?>
<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js"></script>
<script>
  $(function($){ // taken from Manish Jesani. thanks!
    $(".personrole").each(function () {
        var numChars = $(this).text().length;     
        if ((numChars >= 1) && (numChars < 14)) {
            // we dont nee anything because its autosetup. but whatver
        }
        else if ((numChars >= 15) && (numChars < 19)) {
            $(this).css("font-size", "250%");
            $(this).css("top", "100");
        }
        else if ((numChars >= 20) && (numChars < 24)) {
          $(this).css("font-size", "200%");
            $(this).css("top", "105");
        }
        else if ((numChars >= 25) && (numChars < 1000)) {
            $(this).css("font-size", "180%");
            $(this).css("top", "110");
        }
        else if ((numChars >= 25) && (numChars < 100)) {
            $(this).css("font-size", "150%");
            $(this).css("top", "113");
        }
    });
    $(".capaskill").each(function () {
        var numChars = $(this).text().length;     
        if ((numChars >= 1) && (numChars < 20)) {
            // we dont nee anything because its autosetup. but whatver
        }
        else if ((numChars >= 20) && (numChars < 22)) {
            $(this).css("font-size", "28");
        }
        else if ((numChars >= 22) && (numChars < 24)) {
            $(this).css("font-size", "27");
        }
        else if ((numChars >= 24) && (numChars < 26)) {
            $(this).css("font-size", "26");
        }
    });
});
</script>
<link rel="stylesheet" href="/css.css">
</head>
<body style="background-color: black">
<div class="container">
  <img class="playerlistingimg" src="/images/box.png">
  <div> <!-- Faction images -->
  <?php
  $style=array("","235px","296px","353px","410px","467px","524px","581px","640px","697px","754px","811px","868px","925px","982px","1039px","1096px");
   for ($i = 1; $i <= 16; $i++){
    checkrole($i, $style[$i]);
   }?>
  </div>
  <div> <!-- Class images -->
  <?php
  $style=array("","235px","296px","353px","410px","467px","524px","581px","640px","697px","754px","811px","868px","925px","982px","1039px","1096px");
   for ($i = 1; $i <= 16; $i++){
    classimages($i, $style[$i]);
   }?>
  </div>
  <div> <!-- Arrested/Dead images -->
  <?php
  $style=array("","235px","296px","353px","410px","467px","524px","581px","640px","697px","754px","811px","868px","925px","982px","1039px","1096px");
   for ($i = 1; $i <= 16; $i++){
    checkheartbeat($i, $style[$i]);
   }?>
  </div>
  <div class="playerlisting"> <!-- Player List -->
    <table>
      <tr>
        <td style="border-top:30px solid transparent;color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"> <?php printsidebar($sidebarnumber); $sidebarnumber++; ?> </td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
      <tr>
        <td style="color:#<?php checkcolor($colornumber); $colornumber++; ?>"><?php printsidebar($sidebarnumber); $sidebarnumber++; ?></td>
      </tr>
    </table>
    <div><!-- Votes -->
      <?php votes(); ?>
    </div>
  </div>
  <div class="playerinfo">
    <img class="playerinfoimg" src="/images/small.v1.png">
    <img class="playerheaderimg" src="/images/header.png">
    <div class="personrole" style="color:#<?php checkcolornodeath($role);?>"><?php echo $role;?></div>
    <img class="playerrolerimg" src="/images/classes/<?php roleimage($role);?>.png">
    <div class="personcolor"><?php echo $data2[$user][0];?>'s role</div>
  </div>
  <form style="position: absolute;top: 340;left: 2000;" action="" method="post">
   <input type="hidden" name="name" id="name" value="<?php if(empty($asc)){}else{echo $asc;}?>">
   <?php agentbutton() ?>
  </form>
  <div> <!-- Capabilities -->
    <img class="capaboximg" src="/images/box2.png">
    <img class="capaheaderrimg" src="/images/header.png">
    <div class="capabilities">CAPABILITIES</div>
    <div class="capaholder">
      <?php capabilities(); ?>
    </div>
    <?php capaselected(); ?>
  </div>
  <div> <!-- Mailbox -->
      <img class="mailboximg" src="/images/box2.png">
      <img class="mailtriangle" src="/images/header.png">
      <div class="mail">E-MAIL</div>
      <div class="mailholder">
        <?php mail2(); ?>
      </div>
  </div>
  <div class="topopaster"> <!-- Topology -->
    <img class="topoboximg" src="/images/box2.png">
    <img class="topotriangle" src="/images/header.png">
    <div class="topology">TARGET NETWORK TOPOLOGY</div>
    <!-- i dont know how the fuck i am doing this topology. help. -->
  </div>
  <div> <!-- Chatbox -->
    <img class="chatboximg" src="/images/<?php echo $chatbox ?>.png">
    <img class="chattriangle" src="/images/header.png">
    <div class="chat">TERMINAL</div>
    <div class="chatbox">
      <div class="chatholder">
        <?php messages(); ?>
      </div>
    </div>
  </div>
  <div> <!-- TimeBox -->
    <img class="timeboximg" src="/images/timebox.png">
    <?php timebox(); ?>
    <div class="timeboxtimer">69 seconds left</div>
  </div>
  <div> <!-- Buttons -->
    <img class="reportimg" src="/images/report.png" onclick="`Report anything to my discord dm's so i wont miss them: Ping#6175`">
    <img class="powerimg" src="/images/power.png">
    <button class="soundimg" id="musicplayer" onClick="playPause()">
      <audio 
       src="/music/untrusted-soundtrack-<?php music(); ?>-theme.mp3"
       autoplay 
       loop
      ></audio>
    </button>
    <!-- For music player -->
    <script>
      var aud = document.getElementById("musicplayer").children[0];
      var isPlaying = false;
      aud.pause();
      function playPause() {
        if (isPlaying) {
          aud.pause();
          document.getElementById("musicplayer").style.backgroundImage="url('/images/muted.png')";
        } else {
          aud.play();
          document.getElementById("musicplayer").style.backgroundImage="url('/images/sound.png')";
        }
        isPlaying = !isPlaying;
      }
    </script>
    <img class="optionsimg" src="/images/options.png">
  </div>
  <img class="headerimg" src="/images/header.png">
  <div class="etcshadow">/etc/shadow</div>
</div>
</body>
</html>