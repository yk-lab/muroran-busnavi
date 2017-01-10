var __extends = (this && this.__extends) || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
};
var Stops = new StopList();
var StopListBox = (function (_super) {
    __extends(StopListBox, _super);
    function StopListBox(props) {
        return _super.call(this, props) || this;
    }
    StopListBox.prototype.render = function () {
        return React.createElement("ul", { className: "stop-list" }, this.props.stops.map(function (stop) { return React.createElement(StopBox, { stop: stop }); }));
    };
    return StopListBox;
}(React.Component));
var StopBox = (function (_super) {
    __extends(StopBox, _super);
    function StopBox(props) {
        return _super.call(this, props) || this;
    }
    StopBox.prototype.render = function () {
        return React.createElement("li", { className: "stop-item" });
    };
    return StopBox;
}(React.Component));
