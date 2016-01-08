/**
 * Created by user on 1/7/16.
 */
var tabsFn = (function() {

  function init() {
    setHeight();
  }

  function setHeight() {
    var $tabPane = $('.vertical-tab-pane'),
        tabsHeight = $('.vertical-nav-tabs').height();

    $tabPane.css({
      height: tabsHeight
    });
  }

  $(init);
})();
