      function generate_address( username, hostname ) {
        var domain = ".berkeley.edu";
        var atsign = "&#64;";
        var addr = username + atsign + hostname + domain;
        document.write( 
          "<" + "a" + " " + "href=" + "mail" + "to:" + addr + ">" +
          addr +
          "<\/a>");
      }