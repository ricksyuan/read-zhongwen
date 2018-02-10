/**
 * createAugmentedSpanFor(phrase) takes a phrase dictionary and returns a span with tooltip functionality
 */
function createAugmentedSpanFor(phrase) {
  var span = $('<span />').html(phrase["lookup"]);
  var type = phrase["type"];
  span.data("definitions", phrase["definitions"]);
  
  ///////////////
  // Add hover //
  ///////////////
  
  // Highlight character phrases in red (simplified), blue (traditional), or gray (other)
  span.hover(function(){
    // On hover
    $(this).addClass("reading");
    if (type == "traditional") {
      $(this).addClass("traditional");
    } else if (type == "simplified") {
      $(this).addClass("simplified")
    } else if (type == "other") {
      $(this).addClass("other")
    }
                
  }, function(){
    // On exiting hover
    $(this).removeClass("reading");
    $(this).removeClass("traditional");
    $(this).removeClass("simplified");
    $(this).removeClass("other");
    $(this).removeClass("selected");
    $(this).tooltip("dispose"); // Also applies to tap on mobile device
  });
  
  ///////////////
  // Add click //
  ///////////////
  
  // Define span tap or click behavior: show tooltip for phrase when clicked
  span.click(function(){
    // whenever a readable span is clicked
        
    // either clicked on current selected span, or another span
    // if current selected span, then deselect and remove tooltip
    // if not currently selected span, then deselect currently selected and select current
        
    // deselect this span if selected
    if ($(this).hasClass("selected")) {
      $(this).removeClass("selected");
      $(this).tooltip("dispose");
    } else {
            
      // deselect any previously selected spans
      $("span.selected").tooltip("dispose");
      $("span.selected").removeClass("selected");
        
      // select this element
      $(this).addClass("selected");

      // Add tooltip with definitions for traditional or simplified
      var definitions = phrase["definitions"];
      if (definitions != null) {
        // Start with title and ordered list
        var title = $('<ol></ol>').addClass('tooltiporderedlist');

        for (var j = 0; j < definitions.length; j++) {
          var pinyin = definitions[j]["pinyin"];
          var simplified = definitions[j]["simplified"];
          var traditional = definitions[j]["traditional"];
          var definition = definitions[j]["definition"];
          var definition = definitions[j]["definition"];
          var entry = $('<li></li>');
          if (type == "simplified") {
            // Add simplified
            entry.append(`${simplified}`);
            if (traditional != simplified) {
              entry.append(` (${traditional})`);
            }
          } else if (type == "traditional") {
            entry.append(`${traditional}`);
            if (traditional != simplified) {
              entry.append(` --> ${simplified}`);
            }
          }
                
          entry.append(`<br>${pinyin}<br>${definition}`);
          title.append(entry);
        }

        // Create tooltip when tapped or clicked
        $(this).tooltip({title: title, html: true, trigger: "click"}); // only trigger tooltip when clicked, not hover!
        $(this).tooltip("show");
      }
    
    }
  });
    
  return span;
}

/**
 * createAugmentedSpansFor(phrases) takes an array of phrase and returns an array of spans with tooltip functionality.
 */
function createAugmentedSpansFor(phrases) {
    var spans = [];
    for (var i = 0; i < phrases.length; i++) {
        var phrase = phrases[i];
        var span = createAugmentedSpanFor(phrase);
        spans.push(span);
    }
    return spans
}

