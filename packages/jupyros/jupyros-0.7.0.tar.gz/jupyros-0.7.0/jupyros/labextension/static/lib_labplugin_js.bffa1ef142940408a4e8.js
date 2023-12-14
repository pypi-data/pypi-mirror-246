(self["webpackChunk_robostack_jupyter_ros"] = self["webpackChunk_robostack_jupyter_ros"] || []).push([["lib_labplugin_js"],{

/***/ "./lib/defaults.js":
/*!*************************!*\
  !*** ./lib/defaults.js ***!
  \*************************/
/***/ ((module) => {


var DepthCloudModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "DepthCloudModel",
        f: 526.1,
        url: "",
    }
    
    

var GridModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "GridModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "GridView",
        cell_size: 0.5,
        color: "#0181c4",
        num_cells: 20,
    }
    
    

var InteractiveMarkerModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "InteractiveMarkerModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "InteractiveMarkerView",
        menu_font_size: "0.8em",
        ros: null,
        tf_client: null,
        topic: "/basic_controls",
    }
    
    

var LaserScanModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "LaserScanModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "LaserScanView",
        color_map: "",
        color_source: "intensities",
        max_points: 200000,
        message_ratio: 1.0,
        point_ratio: 1.0,
        point_size: 0.05,
        ros: null,
        static_color: "#FF0000",
        tf_client: null,
        topic: "/scan",
    }
    
    

var MarkerModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "MarkerModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "MarkerView",
        lifetime: 0.0,
        path: "/",
        ros: null,
        tf_client: null,
        topic: "/visualization_marker",
    }
    
    

var MarkerArrayClientModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "MarkerArrayClientModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "MarkerArrayClientView",
        path: "/",
        ros: null,
        tf_client: null,
        topic: "/marker_array",
    }
    
    

var OccupancyGridModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "OccupancyGridModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "OccupancyGridView",
        color: "#FFFFFF",
        compression: "cbor",
        continuous: false,
        opacity: 1.0,
        ros: null,
        tf_client: null,
        topic: "/map",
    }
    
    

var PathModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "PathModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "PathView",
        color: "#CC00FF",
        ros: null,
        tf_client: null,
        topic: "/path",
    }
    
    

var PointCloudModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "PointCloudModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "PointCloudView",
        max_points: 200000,
        message_ratio: 2.0,
        point_ratio: 3.0,
        point_size: 0.05,
        ros: null,
        static_color: "#FF0000",
        tf_client: null,
        topic: "/point_cloud",
    }
    
    

var PolygonModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "PolygonModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "PolygonView",
        color: "#CC00FF",
        ros: null,
        tf_client: null,
        topic: "/polygon",
    }
    
    

var PoseModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "PoseModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "PoseView",
        color: "#CC00FF",
        length: 1.0,
        ros: null,
        tf_client: null,
        topic: "/pose",
    }
    
    

var PoseArrayModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "PoseArrayModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "PoseArrayView",
        color: "#CC00FF",
        length: 1.0,
        ros: null,
        tf_client: null,
        topic: "/pose_array",
    }
    
    

var ROSConnectionModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "ROSConnectionModel",
        url: "ws://{hostname}:9090",
    }
    
    

var SceneNodeModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "SceneNodeModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "SceneNodeView",
        frame_id: "/base_link",
        object: null,
        tf_client: null,
    }
    
    

var TFClientModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "TFClientModel",
        angular_treshold: 0.01,
        fixed_frame: "",
        rate: 10.0,
        ros: null,
        translational_treshold: 0.01,
    }
    
    

var URDFModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "URDFModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "URDFView",
        ros: null,
        tf_client: null,
        url: "http://{hostname}:3000",
    }
    
    

var ViewerModelDefaults =     {
        _model_module: "@robostack/jupyter-ros",
        _model_module_version: "^0.6.1",
        _model_name: "ViewerModel",
        _view_module: "@robostack/jupyter-ros",
        _view_module_version: "^0.6.1",
        _view_name: "ViewerView",
        alpha: 1.0,
        background_color: "#FFFFFF",
        height: "100%",
        objects: null,
    }
    
    

module.exports = {
    DepthCloudModelDefaults: DepthCloudModelDefaults,
    GridModelDefaults: GridModelDefaults,
    InteractiveMarkerModelDefaults: InteractiveMarkerModelDefaults,
    LaserScanModelDefaults: LaserScanModelDefaults,
    MarkerArrayClientModelDefaults: MarkerArrayClientModelDefaults,
    MarkerModelDefaults: MarkerModelDefaults,
    OccupancyGridModelDefaults: OccupancyGridModelDefaults,
    PathModelDefaults: PathModelDefaults,
    PointCloudModelDefaults: PointCloudModelDefaults,
    PolygonModelDefaults: PolygonModelDefaults,
    PoseArrayModelDefaults: PoseArrayModelDefaults,
    PoseModelDefaults: PoseModelDefaults,
    ROSConnectionModelDefaults: ROSConnectionModelDefaults,
    SceneNodeModelDefaults: SceneNodeModelDefaults,
    TFClientModelDefaults: TFClientModelDefaults,
    URDFModelDefaults: URDFModelDefaults,
    ViewerModelDefaults: ViewerModelDefaults,
}

    

/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) Wolf Vollprecht, QuantStack                                 //
//                                                                           //
// Distributed under the terms of the BSD 3-Clause License.                  //
//                                                                           //
// The full license is in the file LICENSE, distributed with this software.  //
///////////////////////////////////////////////////////////////////////////////

// Export widget models and views, and the npm package version number.
module.exports = __webpack_require__(/*! ./jupyter-ros.js */ "./lib/jupyter-ros.js");
module.exports.version = __webpack_require__(/*! ../package.json */ "./package.json").version;


/***/ }),

/***/ "./lib/jupyter-ros.js":
/*!****************************!*\
  !*** ./lib/jupyter-ros.js ***!
  \****************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) Wolf Vollprecht, QuantStack                                 //
//                                                                           //
// Distributed under the terms of the BSD 3-Clause License.                  //
//                                                                           //
// The full license is in the file LICENSE, distributed with this software.  //
///////////////////////////////////////////////////////////////////////////////

window.ws = window.WebSocket;
var widgets = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base");
var _ = __webpack_require__(/*! lodash */ "webpack/sharing/consume/default/lodash/lodash");

var ROSLIB = __webpack_require__(/*! roslib */ "./node_modules/roslib/src/RosLib.js");
var ROS3D = __webpack_require__(/*! ros3d */ "webpack/sharing/consume/default/ros3d/ros3d");
var THREE = __webpack_require__(/*! three */ "./node_modules/three/build/three.module.js");

var defaults = __webpack_require__(/*! ./defaults.js */ "./lib/defaults.js")

var widget_defaults = widgets.WidgetModel.prototype.defaults;
var domwidget_defaults = widgets.DOMWidgetModel.prototype.defaults;

var default_serializers = function(names) {
    names = names || ['ros', 'tf_client']

    var named_serializers = {}
    for (let idx in names)
    {
        named_serializers[names[idx]] = { deserialize: widgets.unpack_models }
    }
    return {serializers: _.extend(named_serializers, widgets.WidgetModel.serializers)};
}

var fixup_url = function(url) {
    url = url
        .replace("{hostname}", window.location.hostname)
        .replace("{port}", window.location.port);
    return url;
}

var ROSConnectionModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.ROSConnectionModelDefaults),
    initialize: function() {
        ROSConnectionModel.__super__.initialize.apply(this, arguments);
        this.connection = new ROSLIB.Ros({
          url: fixup_url(this.get('url'))
        });
    },
    get_connection: function() {
        return this.connection;
    }
});

var TFClientModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.TFClientModelDefaults),
    initialize: function() {
        TFClientModel.__super__.initialize.apply(this, arguments);
        this.client = new ROSLIB.TFClient({
          ros: this.get('ros').get_connection(),
          angularThres: this.get('angular_treshold'),
          transThres: this.get('translational_treshold'),
          rate: this.get('rate'),
          fixedFrame: this.get('fixed_frame')
        });
    },
    get_client: function() {
        return this.client;
    },
}, default_serializers(['ros'])
);

var PointCloudModel = widgets.WidgetModel.extend({
    defaults: _.extend(widgets.WidgetModel.prototype.defaults(), defaults.PointCloudModelDefaults),
}, default_serializers());

var OccupancyGridModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.OccupancyGridDefaults),
}, default_serializers());

var SceneNodeModel = widgets.WidgetModel.extend({
    defaults: _.extend(widgets.WidgetModel.prototype.defaults(), defaults.SceneNodeModelDefaults),
}, default_serializers(['tf_client', 'object']));

var OccupancyGridView = widgets.WidgetView.extend({
    initialize: function(args) {
        OccupancyGridView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
    },
    render: function() {
        this.three_color = new THREE.Color(this.model.get('color'));
        this.rgb_color = {r: this.three_color.r * 255, 
                          g: this.three_color.g * 255,
                          b: this.three_color.b * 255};

        this.view = new ROS3D.OccupancyGridClient({
            rootObject: this.viewer.scene,
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            color: this.rgb_color,
            compression: this.model.get('compression'),
            continuous: this.model.get('continuous'),
            opacity: this.model.get('opacity')
        });
    }
});

var InteractiveMarkerModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.InteractiveMarkerDefaults),
},
default_serializers()
);

var InteractiveMarkerView = widgets.WidgetView.extend({
    initialize: function(args) {
        InteractiveMarkerView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
    },
    render: function() {
        this.view = new ROS3D.InteractiveMarkerClient({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            menuFontSize: this.model.get('menu_font_size'),
            camera: this.viewer.camera,
            rootObject: this.viewer.selectableObjects,
        });
    }
});

var PoseArrayModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.PoseArrayDefaults),
},
default_serializers()
);

var PoseArrayView = widgets.WidgetView.extend({
    initialize: function(args) {
        PoseArrayView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on("change:length", () => { this.view.length = this.model.get('length') });
        this.model.on("change:color", () => { this.view.color = this.model.get('color'); });
    },
    render: function() {
        this.view = new ROS3D.PoseArray({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            color: this.model.get('color'),
            length: this.model.get('length'),
            rootObject: this.viewer.scene,
        });
    }
});

var PoseModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.PoseModelDefaults),
},
default_serializers()
);

var PoseView = widgets.WidgetView.extend({
    initialize: function(args) {
        PoseView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on("change:length", () => { this.view.length = this.model.get('length') });
        this.model.on("change:color", () => { this.view.color = this.model.get('color'); });
    },
    render: function() {
        this.view = new ROS3D.Pose({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            color: this.model.get('color'),
            length: this.model.get('length'),
            rootObject: this.viewer.scene,
        });
    }
});

var PathModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.PathModelDefaults),
},
default_serializers()
);

var PathView = widgets.WidgetView.extend({
    initialize: function(args) {
        PathView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on("change:color", () => { this.view.color = this.model.get('color'); });
    },
    render: function() {
        this.view = new ROS3D.Path({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            color: this.model.get('color'),
            rootObject: this.viewer.scene,
        });
    }
});

var PolygonModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.PolygonModelDefaults),
},
default_serializers()
);

var PolygonView = widgets.WidgetView.extend({
    initialize: function(args) {
        PolygonView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on("change:color", () => { this.view.color = this.model.get('color'); });
    },
    render: function() {
        this.view = new ROS3D.Polygon({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            color: this.model.get('color'),
            rootObject: this.viewer.scene,
        });
    }
});

var LaserScanModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.LaserScanModelDefaults),
},
default_serializers()
);

var toMaterial = function(pointSize, color) {
    return { size: pointSize, color: new THREE.Color(color) };
};

var LaserScanView = widgets.WidgetView.extend({
    initialize: function(args) {
        LaserScanView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on("change", this.trigger_rerender, this);
    },
    render: function() {
        if (this.model.get('color_map')) {
            this.color_map_function = eval(this.model.get('color_map'))
        }
        this.view = new ROS3D.LaserScan({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            rootObject: this.viewer.scene,
            messageRatio: this.model.get('message_ratio'),
            max_pts: this.model.get('max_points'),
            pointRatio: this.model.get('point_ratio'),
            material: toMaterial(this.model.get('point_size'), this.model.get('static_color')),
            colorsrc: this.model.get('color_source'),
            colormap: this.color_map_function || undefined
        });
    },
    remove: function() {
        this.viewer.scene.remove(this.view.points.sn);
    },
    trigger_rerender: function() {
        this.remove();
        this.render();
    }
});

var MarkerModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.MarkerDefaults),
},
default_serializers()
);

var MarkerView = widgets.WidgetView.extend({
    initialize: function(args) {
        MarkerView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
    },
    render: function() {
        this.view = new ROS3D.MarkerClient({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            path: this.model.get('path'),
            lifetime: this.model.get('lifetime'),
            rootObject: this.viewer.scene,
        });
    }
});

var MarkerArrayModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.MarkerArrayDefaults),
},
default_serializers()
);

var MarkerArrayView = widgets.WidgetView.extend({
    initialize: function(args) {
        MarkerArrayView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        // this.model.on("change", this.trigger_rerender, this);
    },
    render: function() {
        this.view = new ROS3D.MarkerArrayClient({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            path: this.model.get('path'),
            rootObject: this.viewer.scene,
        });
    }
});

var GridModel = widgets.WidgetModel.extend({
    defaults: _.extend(widgets.WidgetModel.prototype.defaults(), defaults.GridModelDefaults)
});

var URDFModel = widgets.WidgetModel.extend({
    defaults: _.extend(widgets.WidgetModel.prototype.defaults(), defaults.URDFModelDefaults),
},
default_serializers()
);

var URDFView = widgets.WidgetView.extend({
    initialize: function(parms) {
        URDFView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        // this.model.on('change', this.trigger_rerender, this);
    },
    render: function() {
        this.view = new ROS3D.UrdfClient({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            rootObject: this.viewer.scene,
            path: fixup_url(this.model.get('url'))
        });
    },
    trigger_rerender: function() {
        this.remove();
        this.render();
    },
    remove: function() {
        this.viewer.scene.remove(this.view);
    }
});

var ViewerModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), defaults.ViewerModelDefaults)
},
default_serializers(['objects', 'layout'])
);

var PointCloudView = widgets.WidgetView.extend({
    initialize: function(parms) {
        PointCloudView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
    },
    render: function() {
        // if (this.model.get('color_map')) {
        //     this.color_map_function = new Function(this.model.get('color_source'), 'THREE', this.model.get('color_map'));
        //     this.color_map_apply = function() { args = arguments; args.push(THREE); this.color_map_apply.apply(null, args); }
        //     material = { size: this.model.get('point_size'), sizeAttenuation: false };
        // }
        // else {
        //     material = toMaterial(this.model.get('point_size'), this.model.get('static_color'));
        // }

        this.view = new ROS3D.PointCloud2({
            ros: this.model.get('ros').get_connection(),
            tfClient: this.model.get('tf_client').get_client(),
            topic: this.model.get('topic'),
            rootObject: this.viewer.scene,
            messageRatio: this.model.get('message_ratio'),
            max_pts: this.model.get('max_points'),
            pointRatio: this.model.get('point_ratio'),
            material: toMaterial(this.model.get('point_size'), this.model.get('static_color'))
            // colorsrc: this.model.get('color_source'),
            // colormap: this.color_map_apply || undefined
        });
    },
    // remove: function() {
    //     this.viewer.scene.remove(this.view.points.sn);
    // }
});

var DepthCloudModel = widgets.WidgetModel.extend({
    defaults: _.extend(widget_defaults(), defaults.DepthCloudModelDefaults),
    initialize: function() {
        DepthCloudModel.__super__.initialize.apply(this, arguments);
        this.depth_cloud = new ROS3D.DepthCloud({
            url: this.get('url'),
            f: this.get('f')
        });
        this.depth_cloud.startStream();
    },
    get_threejs_obj: function() {
        return this.depth_cloud;
    },
});

var SceneNodeView = widgets.WidgetView.extend({
    initialize: function(parms) {
        SceneNodeView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on('change', this.trigger_rerender, this);
    },
    render: function() {
        this.view = new ROS3D.SceneNode({
            frameID: this.model.get('frame_id'),
            tfClient: this.model.get('tf_client').get_client(),
            object: this.model.get('object').get_threejs_obj()
        });
        this.viewer.scene.add(this.view);
    },
    trigger_rerender: function() {
        this.remove();
        this.render();
    },
    remove: function() {
        this.viewer.scene.remove(this.view);
    }
});

var GridView = widgets.WidgetView.extend({
    initialize: function(parms) {
        GridView.__super__.initialize.apply(this, arguments);
        this.viewer = this.options.viewer;
        this.model.on('change', this.trigger_rerender, this);
    },
    render: function() {
        this.grid_view = new ROS3D.Grid({
            color: this.model.get('color'),
            cellSize: this.model.get('cell_size'),
            num_cells: this.model.get('num_cells')
        });
        this.viewer.addObject(this.grid_view);
    },
    trigger_rerender: function() {
        this.remove();
        this.render();
    },
    remove: function() {
        this.viewer.scene.remove(this.grid_view);
    }
});

// Custom View. Renders the widget model.
var ViewerView = widgets.DOMWidgetView.extend({
    render: function() {
        var unique_id = (new Date).getTime().toString() + Math.floor(Math.random() * Math.floor(9999)).toString();
        this.el.id = unique_id + 'ROS_VIEWER';

        this.model.on("change:background_color", this.background_color_change, this);
        this.model.on("change:alpha", this.background_color_change, this);

        this.displayed.then(() => {
           this.init_viewer();
        });
    },

    add_object: function (model) {
        return this.create_child_view(model, {
            viewer: this.viewer,
        });
    },
    remove_object: function (view) {
        view.remove();
    },
    objects_changed: function(msg) {
        this.object_views.update(msg.changed.objects);
    },
    trigger_resize: function() {
        this.viewer.resize(this.el.clientWidth, this.el.clientHeight)
    },
    processPhosphorMessage: function(msg) {
        ViewerView.__super__.processPhosphorMessage.apply(this, arguments);
        if (msg.type == 'resize') {
            this.trigger_resize();
        }
    },
    background_color_change: function() {
        this.viewer.renderer.setClearColor(this.model.get('background_color'), this.model.get('alpha'))
    },
    init_viewer: function() {
        var height = this.model.get('layout').get('height');
        if (height === null || height == 'auto') {
            height = 400;
        }
        else {
            height = parseInt(height)
        }

        this.viewer = new ROS3D.Viewer({
            divID: this.el.id,
            width: this.el.clientWidth,
            height: height,
            antialias: this.model.get('antialias'),
            background: this.model.get('background_color')
        });

        window.addEventListener("resize", () => {
           this.viewer && this.trigger_resize();
        });

        this.model.on("change:objects", this.objects_changed, this);
        this.object_views = new widgets.ViewList(this.add_object, this.remove_object, this);
        this.object_views.update(this.model.get('objects'));
     }
});


module.exports = {
    ROSConnectionModel: ROSConnectionModel,
    TFClientModel: TFClientModel,
    PointCloudModel: PointCloudModel,
    PointCloudView: PointCloudView,
    MarkerModel: MarkerModel,
    MarkerView: MarkerView,
    MarkerArrayModel: MarkerArrayModel,
    MarkerArrayView: MarkerArrayView,
    OccupancyGridModel: OccupancyGridModel,
    OccupancyGridView: OccupancyGridView,
    InteractiveMarkerModel: InteractiveMarkerModel,
    InteractiveMarkerView: InteractiveMarkerView,
    GridModel: GridModel,
    GridView: GridView,
    URDFModel: URDFModel,
    URDFView: URDFView,
    PoseArrayModel: PoseArrayModel,
    PoseArrayView: PoseArrayView,
    PoseModel: PoseModel,
    PoseView: PoseView,
    PathModel: PathModel,
    PathView: PathView,
    PolygonModel: PolygonModel,
    PolygonView: PolygonView,
    LaserScanModel: LaserScanModel,
    LaserScanView: LaserScanView,
    SceneNodeModel: SceneNodeModel,
    SceneNodeView: SceneNodeView,
    DepthCloudModel: DepthCloudModel,
    ViewerModel: ViewerModel,
    ViewerView: ViewerView
};


/***/ }),

/***/ "./lib/labplugin.js":
/*!**************************!*\
  !*** ./lib/labplugin.js ***!
  \**************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

///////////////////////////////////////////////////////////////////////////////
// Copyright (c) Wolf Vollprecht, QuantStack                                 //
//                                                                           //
// Distributed under the terms of the BSD 3-Clause License.                  //
//                                                                           //
// The full license is in the file LICENSE, distributed with this software.  //
///////////////////////////////////////////////////////////////////////////////

var index_module = __webpack_require__(/*! ./index.js */ "./lib/index.js");
var base = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base");

module.exports = {
  id: '@robostack/jupyter-ros',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
    widgets.registerWidget({
        name: '@robostack/jupyter-ros',
        version: index_module.version,
        exports: index_module
    });
  },
  autoStart: true
};



/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"@robostack/jupyter-ros","version":"0.7.0-a0","description":"Jupyter widgets for the ROS ecosystem.","homepage":"https://github.com/wolfv/jupyter-ros.git","author":{"name":"Wolf Vollprecht","email":"w.vollprecht@gmail.com"},"license":"BSD-3-Clause","main":"lib/labplugin.js","repository":{"type":"git","url":"https://github.com/wolfv/jupyter-ros.git"},"keywords":["jupyter","widgets","ipython","ipywidgets","jupyterlab-extension"],"files":["lib/**/*.js","dist/*.js"],"scripts":{"clean":"rimraf dist/ ../jupyros/nbextension ../jupyros/labextension","build":"jlpm run build:lib && jlpm run build:labextension:dev","build:lib":"webpack","build:prod":"jlpm run clean && jlpm run build:lib && jlpm run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","install:extension":"jlpm run build","watch":"run-p watch:src && watch:labextension","watch:src":"webpack --watch","watch:labextension":"jupyter labextension watch .","test":"echo \\"Error: no test specified\\" && exit 1","prepublish":"webpack"},"devDependencies":{"@jupyterlab/builder":"^3.0.1","npm-run-all":"^4.1.5","rimraf":"^4.1.2","webpack":"^5.75.0","webpack-cli":"^5.0.1"},"dependencies":{"@jupyter-widgets/base":"^2.0.1 || ^3 || ^4","lodash":"^4.17.21","ros3d":"^1.0.0"},"jupyterlab":{"extension":"lib/labplugin.js","outputDir":"../jupyros/labextension"}}');

/***/ })

}]);
//# sourceMappingURL=lib_labplugin_js.bffa1ef142940408a4e8.js.map