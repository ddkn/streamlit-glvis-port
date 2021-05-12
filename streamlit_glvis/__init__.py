import io
import os
import streamlit as st
import streamlit.components.v1 as components
try:
    from mfem._ser.mesh import Mesh
    from mfem._ser.gridfunc import GridFunction
except ImportError:
    Mesh = object
    GridFunction = object

_RELEASE = False
# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("streamlit_glvis"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "streamlit_glvis",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_glvis", path=build_dir)

def to_stream(mesh: Mesh, gf: GridFunction = None) -> str:
    sio = io.StringIO()
    sio.write("solution\n" if gf is not None else "mesh\n")
    mesh.WriteToSTream(sio)
    if gf:
        gf.WriteToStream(sio)
    return sio.getvalue()

# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def streamlit_glvis(name, key=None):
    """Create a new instance of "streamlit_glvis".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(name=name, key=key, default=0)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


def to_stream(mesh: Mesh, gf: GridFunction = None) -> str:
    sio = io.StringIO()
    sio.write("solution\n" if gf is not None else "mesh\n")
    mesh.WriteToSTream(sio)
    if gf:
        gf.WriteToStream(sio)
    return sio.getvalue()
   
#def glvis(datastream, width, height, key=None):
#    # GLVis/glvis-js code, see included LICENSE.glvis-js BSD3 License
#    components.html(f"""
#    <link rel="icon" type="image/png" href="https://glvis.org/img/favicon.ico" />
#    <link href="https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900" rel="stylesheet" />
#    <link href="https://cdn.jsdelivr.net/npm/@mdi/font@4.x/css/materialdesignicons.min.css" rel="stylesheet" />
#    <link href="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css" rel="stylesheet" />
#    <script src="https://glvis.org/live/src/glvis.js"></script>
#    <script src="https://glvis.org/live/src/index.js"></script>
#    <script src="https://glvis.org/live/src/helper.js"></script>
#    <div id="app" ref="app">
#      <v-app>
#        <v-main>
#          <div class="main-container">
#            <div class="menu-indicator-space" @mouseover="menuActive = true"
#              @mouseout="if (!touchDevice) menuActive = false;"></div>
#            <transition name="fade">
#              <div v-show="menuActive" @mouseover="menuActive = true">
#                <!-- Buttons in top left -->
#                <div class="overlay-left">
#                  <v-tooltip transition="fade" bottom><template v-slot:activator="{ on, attrs }">
#                      <input id="fileUpload" ref="fileUpload" type="file" hidden v-on:change="openLocalFile" />
#                      <v-btn class="overlay-button" small elevation="2" fab @click="selectLocalFile" v-bind="attrs"
#                        v-on="on">
#                        <v-icon>mdi-folder-open</v-icon>
#                      </v-btn>
#                    </template><span>Load local file</span>
#                  </v-tooltip>
#                     <!-- Websocket dialog -->
#                  <v-dialog v-model="websocketDialogActive" width="300">
#                    <template v-slot:activator="{ on: dialog, attrs }">
#                      <v-tooltip transition="fade" bottom>
#                        <template v-slot:activator="{ on: tooltip }">
#                          <v-btn class="overlay-button" small elevation="2" fab v-bind="attrs"
#                            v-on="{ ...tooltip, ...dialog }">
#                            <v-icon>mdi-lan-connect</v-icon>
#                          </v-btn>
#                        </template>
#                        <span>Connect to socket</span>
#                      </v-tooltip>
#                    </template>
#                    <v-card>
#                      <v-card-title class="headline grey lighten-2">
#                        Connect to socket
#                      </v-card-title>
#                      <v-spacer></v-spacer>
#                      <v-card-text>
#                        <v-form ref="socketForm" lazy-validation>
#                          <v-text-field v-model="socketHost" label="Host" required></v-text-field>
#                          <v-text-field v-model="socketPort" label="Port" required></v-text-field>
#                          <v-btn @click="connectWebsocket">
#                            {{ connectWebsocketButtonLabel }}
#                          </v-btn>
#                        </v-form>
#                      </v-card-text>
#                    </v-card>
#                  </v-dialog>
#                     <v-tooltip v-if="logMode" transition="fade" bottom><template v-slot:activator="{ on, attrs }">
#                      <v-btn class="overlay-button" small elevation="2" fab @click="logWindowActive = true" v-bind="attrs"
#                        v-on="on">
#                        <v-icon>mdi-script</v-icon>
#                      </v-btn>
#                    </template><span>View log</span></v-tooltip>
#                  <v-tooltip transition="fade" bottom><template v-slot:activator="{ on, attrs }">
#                      <v-btn class="overlay-button" small elevation="2" fab @click="helpWindowActive = !helpWindowActive"
#                        v-bind="attrs" v-on="on">
#                        <v-icon>mdi-help</v-icon>
#                      </v-btn>
#                    </template><span>Help</span></v-tooltip>
#                </div>
#                   <!-- Overlay middle -->
#                <div class="overlay-middle">
#                  <v-icon class="outlined" v-if="glvStreamIsPaused" @click="glvStreamIsPaused = false" large>mdi-pause
#                  </v-icon>
#                </div>
#                   <!-- Buttons in top right -->
#                <div class="overlay-right">
#                  <!-- Examples dialog -->
#                  <v-dialog v-model="examplesDialogActive" scrollable width="275px">
#                    <template v-slot:activator="{ on: dialog, attrs }">
#                      <v-tooltip transition="fade" bottom>
#                        <template v-slot:activator="{ on: tooltip }">
#                          <v-btn class="overlay-button" small elevation="2" fab v-bind="attrs"
#                            v-on="{ ...tooltip, ...dialog }">
#                            <v-icon>mdi-shape</v-icon>
#                          </v-btn>
#                        </template>
#                        <span>Examples</span>
#                      </v-tooltip>
#                    </template>
#                    <v-card>
#                      <v-card-title class="headline grey lighten-2">
#                        Examples
#                      </v-card-title>
#                      <v-spacer></v-spacer>
#                      <v-card-text v-if="glvIsLoading" class="text-center">
#                        <v-progress-circular v-if="glvIsLoading" :size="70" :width="7" color="primary" indeterminate>
#                        </v-progress-circular>
#                      </v-card-text>
#                      <v-card-text v-else class="text-left">
#                        <v-container>
#                          <v-row v-for="example in examples">
#                            <v-col>
#                              <v-btn :key="example.name" color="default" class="overlay-button" small outlined text
#                                elevation="0" @click="loadUrl(example.url)">
#                                <v-icon left>mdi-shape</v-icon>{{ example.name
#                                }}
#                              </v-btn>
#                            </v-col>
#                          </v-row>
#                        </v-container>
#                      </v-card-text>
#                    </v-card>
#                  </v-dialog>
#                     <v-tooltip transition="fade" bottom><template v-slot:activator="{ on, attrs }">
#                      <v-btn class="overlay-button" small elevation="2" fab
#                        @click="controlWindowActive = !controlWindowActive" v-bind="attrs" v-on="on">
#                        <v-icon>mdi-settings</v-icon>
#                      </v-btn>
#                    </template><span>Visualization controls</span></v-tooltip>
#                  <v-tooltip transition="fade" bottom><template v-slot:activator="{ on, attrs }">
#                      <v-btn class="overlay-button" small elevation="2" fab @click="toggleFullscreen" v-bind="attrs"
#                        v-on="on">
#                        <v-icon>mdi-aspect-ratio</v-icon>
#                      </v-btn>
#                    </template><span>Fullscreen mode</span></v-tooltip>
#                </div>
#              </div>
#            </transition>
#               <!-- Log window -->
#            <!-- prettier-ignore -->
#            <v-card id="log-window" v-if="logWindowActive" class="help-container" elevation="2">
#              <v-btn elevation="0" x-small fab @click="logWindowActive = false">
#                <v-icon>mdi-close</v-icon>
#              </v-btn>
#              <div style="font-size: xx-small; width:70ch; max-width: 100%; overflow-x: hidden;">
#                <span v-html="logString"></span>
#              </div>
#            </v-card>
#               <!-- Help window -->
#            <!-- prettier-ignore -->
#            <v-card id="help-window" v-if="helpWindowActive" class="help-container" elevation="2">
#              <v-btn elevation="0" x-small fab @click="helpWindowActive = false">
#                <v-icon>mdi-close</v-icon>
#              </v-btn>{{ helpString }}
#              <!-- -->
#              <template>
#                <v-footer padless outlined elevation=0 rounded>
#                  <v-col class="text-center">Powered by <a href="https://glvis.org">GLVis</a><br>Contact us on <a
#                      href="https://github.com/glvis/glvis-js">GitHub</a>
#                  </v-col>
#                </v-footer>
#              </template>
#            </v-card>
#               <!-- Visualization Vontrol window -->
#            <v-card id="control-window" v-if="controlWindowActive" class="control-container" elevation="2">
#              <v-btn elevation="0" x-small fab @click="controlWindowActive = false">
#                <v-icon>mdi-close</v-icon>
#              </v-btn>
#              <template>
#                <!-- Mesh section -->
#                <v-expansion-panels flat dense>
#                  <v-expansion-panel v-for="(item,i) in 1" :key="i">
#                    <v-expansion-panel-header> Mesh </v-expansion-panel-header>
#                    <v-expansion-panel-content>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('a')">
#                          <v-icon left>mdi-axis-arrow</v-icon>Axis
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('m')">
#                          <v-icon left>mdi-grid</v-icon>Mesh
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('e')">
#                          <v-icon left>mdi-checkerboard</v-icon>Elements
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('o')">
#                          <v-icon left>mdi-blur</v-icon>Resolution
#                        </v-btn>
#                      </v-row>
#                    </v-expansion-panel-content>
#                  </v-expansion-panel>
#                </v-expansion-panels>
#                <!-- Colors section -->
#                <v-expansion-panels flat dense>
#                  <v-expansion-panel v-for="(item,i) in 1" :key="i">
#                    <v-expansion-panel-header>
#                      Colors
#                    </v-expansion-panel-header>
#                    <v-expansion-panel-content>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('p')">
#                          Colormap
#                        </v-btn>
#                        &nbsp;&nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('P')">
#                          <v-icon center>mdi-arrow-left</v-icon>
#                        </v-btn>
#                        &nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('p')">
#                          <v-icon center>mdi-arrow-right</v-icon>
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('T')">
#                          <v-icon left>mdi-cisco-webex</v-icon>Material
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('l')">
#                          <v-icon left>mdi-lightbulb-on-outline</v-icon>Light
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('c')">
#                          <v-icon left>mdi-eyedropper</v-icon>Colorbar
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('g')">
#                          <v-icon left>mdi-invert-colors</v-icon>Background
#                        </v-btn>
#                      </v-row>
#                    </v-expansion-panel-content>
#                  </v-expansion-panel>
#                </v-expansion-panels>
#                <!-- Position section -->
#                <v-expansion-panels flat dense>
#                  <v-expansion-panel v-for="(item,i) in 1" :key="i">
#                    <v-expansion-panel-header>
#                      Position
#                    </v-expansion-panel-header>
#                    <v-expansion-panel-content>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('R')">
#                          <v-icon left>mdi-square-outline</v-icon>2D
#                        </v-btn>
#                        &nbsp;&nbsp;
#                        <v-btn small outlined elevation="0" @click="sendKey('r')">
#                          <v-icon left>mdi-cube-outline</v-icon>3D
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="sendKey('j')">
#                          <v-icon left>mdi-perspective-less</v-icon>Perspective
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined @click="sendKey('*')">Zoom</v-btn>
#                        &nbsp;&nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('*')">
#                          <v-icon center>mdi-magnify-plus-outline</v-icon>
#                        </v-btn>
#                        &nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('/')">
#                          <v-icon center>mdi-magnify-minus-outline</v-icon>
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined @click="sendKey('+')">Stretch</v-btn>
#                        &nbsp;&nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('+')">
#                          <v-icon center>mdi-arrow-collapse-up</v-icon>
#                        </v-btn>
#                        &nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('-')">
#                          <v-icon center>mdi-arrow-collapse-down</v-icon>
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined @click="sendKey('.')">Spin</v-btn>
#                        &nbsp;&nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey('0')">
#                          <v-icon center>mdi-axis-z-rotate-clockwise</v-icon>
#                        </v-btn>
#                        &nbsp;
#                        <v-btn x-small fab elevation="0" @click="sendKey(13)">
#                          <v-icon center>mdi-axis-z-rotate-counterclockwise</v-icon>
#                        </v-btn>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <!-- <v-btn small outlined @click="sendKey('5')">Rotate</v-btn> -->
#                        <!-- &nbsp; -->
#                        <v-card elevation="0">
#                          <v-btn x-small fab elevation="0" @click="sendKey('7')">
#                            <v-icon center>mdi-arrow-top-left</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('8')">
#                            <v-icon center>mdi-arrow-up</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('9')">
#                            <v-icon center>mdi-arrow-top-right</v-icon>
#                          </v-btn>
#                          <br />
#                          <v-btn x-small fab elevation="0" @click="sendKey('4')">
#                            <v-icon center>mdi-arrow-left</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('5')">
#                            <v-icon center>mdi-adjust</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('6')">
#                            <v-icon center>mdi-arrow-right</v-icon>
#                          </v-btn>
#                          <br />
#                          <v-btn x-small fab elevation="0" @click="sendKey('1')">
#                            <v-icon center>mdi-arrow-bottom-left</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('2')">
#                            <v-icon center>mdi-arrow-down</v-icon>
#                          </v-btn>
#                          <v-btn x-small fab elevation="0" @click="sendKey('3')">
#                            <v-icon center>mdi-arrow-bottom-right</v-icon>
#                          </v-btn>
#                        </v-card>
#                      </v-row>
#                    </v-expansion-panel-content>
#                  </v-expansion-panel>
#                </v-expansion-panels>
#                <!-- Animation section -->
#                <v-expansion-panels flat dense>
#                  <v-expansion-panel v-for="(item,i) in 1" :key="i">
#                    <v-expansion-panel-header>
#                      Animation
#                    </v-expansion-panel-header>
#                    <v-expansion-panel-content>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-slider prepend-icon="mdi-clock" min="0" max="100" v-model="streamDelay"></v-slider>
#                      </v-row>
#                      <v-row aling="center" justify="center" dense class="pa-md-2">
#                        <v-btn small outlined elevation="0" @click="updateCanvasSize">
#                          <v-icon left>mdi-reload</v-icon>Redraw
#                        </v-btn>
#                      </v-row>
#                    </v-expansion-panel-content>
#                  </v-expansion-panel>
#                </v-expansion-panels>
#              </template>
#            </v-card>
#               <div v-if="glvIsInitializing" class="glvis-window-loading">
#              <v-progress-circular :size="70" :width="7" color="primary" indeterminate>
#              </v-progress-circular>
#            </div>
#            <div v-show="!glvIsInitializing" id="glvis-window" v-doubletap="(e) => onDoubleTap(e)"></div>
#          </div>
#        </v-main>
#      </v-app>
#    </div>
#    <script src="https://cdn.jsdelivr.net/npm/vue@2.6.12"></script>
#    <script src="https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.js"></script>
#    <script src="https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js"></script>
#    <script src="https://cdnjs.cloudflare.com/ajax/libs/async/3.2.0/async.min.js"></script>
#    <script>
#      Vue.config.devtools = true;
#    
#      Vue.directive("doubletap", {
#        bind: function (el, binding) {
#          if (typeof binding.value === "function") {
#            const mc = new Hammer.Manager(el);
#            mc.add(new Hammer.Tap({ event: 'doubletap', taps: 2, interval: 1500, posThresholdL: 50 }));
#            mc.on("doubletap", binding.value);
#          }
#        }
#      });
#    
#      var host = window.location.hostname;
#      if (host === "127.0.0.1" || host === "glvis.org") { host = "localhost" }
#      console.log(`host = ${host}`);
#    
#      const touch = matchMedia('(hover: none), (pointer: coarse)').matches;
#      console.log(`touch = ${touch}`);
#    
#      var app = new Vue({
#        el: "#app",
#        vuetify: new Vuetify(),
#        data: {
#          touchDevice: touch,
#          menuActive: true,
#          examplesDialogActive: false,
#          websocketDialogActive: false,
#          logWindowActive: false,
#          connectWebsocketButtonLabel: "Connect",
#          socketHost: host,
#          socketPort: "8080",
#          controlWindowActive: false,
#          helpWindowActive: false,
#          fullScreenMode: false,
#          glv: null,
#          glvSocket: null,
#          glvSocketQueue: undefined,
#          glvIsLoading: true,
#          glvIsInitializing: true,
#          glvStreamIsPaused: false,
#          glvis_window_div: null,
#          uws_timeout_handle: null,
#          helpString: "",
#          logString: "",
#          experimentalMode: false,
#          logMode: false,
#          streamDelay: 0,
#          defaultExample: 15,
#          examples: [
#            {
#              name: "MFEM Example 1",
#              url: "../data/ex1.saved",
#            },
#            {
#              name: "MFEM Example 2",
#              url: "../data/ex2.saved",
#            },
#            {
#              name: "MFEM Example 3",
#              url: "../data/ex3.saved",
#            },
#            {
#              name: "MFEM Example 5",
#              url: "../data/ex5.saved",
#            },
#            {
#              name: "MFEM Example 9",
#              url: "../data/ex9.saved",
#            },
#            {
#              name: "MFEM Example 27",
#              url: "../data/ex27.saved",
#            },
#            {
#              name: "Capacitor",
#              url: "../data/capacitor.saved",
#            },
#            {
#              name: "Distance",
#              url: "../data/distance.saved",
#            },
#            {
#              name: "Klein Bottle",
#              url: "../data/klein-bottle.saved",
#            },
#            {
#              name: "Laghos",
#              url: "../data/laghos.saved",
#            },
#            {
#              name: "Mesh Explorer",
#              url: "../data/mesh-explorer.saved",
#            },
#            {
#              name: "MFEM Logo",
#              url: "../data/mfem-logo.saved",
#            },
#            {
#              name: "Minimal Surface",
#              url: "../data/minimal-surface.saved",
#            },
#            {
#              name: "Mobius Strip",
#              url: "../data/mobius-strip.saved",
#            },
#            {
#              name: "Navier",
#              url: "../data/navier.saved",
#            },
#            {
#              name: "Quad (default)",
#              url: "../data/quad.saved",
#            },
#            {
#              name: "Remhos",
#              url: "../data/remhos.saved",
#            },
#            {
#              name: "Shaper",
#              url: "../data/shaper.saved",
#            },
#            {
#              name: "Snake",
#              url: "../data/snake.saved",
#            },
#          ],
#        },
#        mounted: function () {
#          var log = new URLSearchParams(document.location.search).get("log");
#          if (log === "true") {
#            this.logMode = true;
#            //var log = document.getElementById("log-window");
#            augmentLoggers(s => this.logString += s);
#          }
#    
#          this.glvis_window_div = document.getElementById("glvis-window");
#          this.glv = new glvis.State(this.glvis_window_div, 1, 1);
#    
#          this.glv.registerNewStreamCallback((state) => {
#            state.getHelpString().then((s) => {
#              this.helpString = s;
#            });
#          });
#    
#          var stream = new URLSearchParams(document.location.search).get("stream");
#          if (stream) {
#            console.log(`loading stream from ${stream}`);
#            this.glv.loadUrl(stream).then(() => {
#              this.glvIsInitializing = false;
#            });
#          } else {
#            this.glv.loadUrl(this.examples[this.defaultExample].url).then(() => {
#              this.glvIsInitializing = false;
#            });
#          }
#    
#          var experimental = new URLSearchParams(document.location.search).get(
#            "experimental"
#          );
#          if (experimental) {
#            this.experimentalMode = true;
#          }
#    
#          this.updateCanvasSize();
#    
#          window.addEventListener("resize", () => {
#            this.updateCanvasSize();
#          });
#    
#          window.addEventListener("orientationchange", () => {
#            this.updateCanvasSize();
#          });
#    
#          window.addEventListener("fullscreenchange", () => {
#            this.updateCanvasSize();
#          });
#    
#          // Event sentinel variable
#          window.addEventListener("keypress", (event) => {
#            if (event.keyCode === 32) {
#              this.glvStreamIsPaused = !this.glvStreamIsPaused;
#            }
#            else if (event.keyCode === 72 || event.keyCode === 104) {
#              this.helpWindowActive = !this.helpWindowActive;
#            } else {
#              this.glv.sendKey(
#                event.keyCode,
#                event.ctrlKey,
#                event.shiftKey,
#                event.altKey
#              );
#            }
#          });
#    
#          window.addEventListener("keydown", (event) => {
#            const code = event.keyCode;
#            // just function keys
#            if (code >= 112 && code <= 123) {
#              const fn_key_offset = 112;
#              const fn_key_sdl_offset = 1073741882;
#              const offset = fn_key_sdl_offset - fn_key_offset;
#              this.glv.sendKey(
#                event.keyCode + offset,
#                event.ctrlKey,
#                event.shiftKey,
#                event.altKey
#              );
#            }
#          });
#    
#          this.glvSocketQueue = async.queue(async (msg) => {
#            while (this.glvStreamIsPaused) {
#              await new Promise((r) => setTimeout(r, 500));
#            }
#            await this.glv.updateStream(msg);
#            if (msg.endsWith("pause\n")) {
#              this.glvStreamIsPaused = true;
#              console.log("pausing");
#            }
#            await new Promise((r) => setTimeout(r, 50 + this.streamDelay * 10));
#          });
#    
#          this.glvIsLoading = false;
#        },
#        watch: {
#          examplesDialogActive: function (v) {
#            if (v && !this.touchDevice) {
#              this.menuActive = false;
#            }
#          },
#          websocketDialogActive: function (v) {
#            if (v && !this.touchDevice) {
#              this.menuActive = false;
#            }
#          },
#        },
#        methods: {
#          updateCanvasSize: function () {
#            [w, h] = windowDim();
#            this.glv.setSize(w, h);
#          },
#          loadUrl: async function (url, keys) {
#            this.glvIsLoading = true;
#            this.glv.loadUrl(url).then(() => {
#              this.examplesDialogActive = false;
#              setTimeout(() => {
#                this.glvIsLoading = false;
#              }, 500);
#            });
#    
#            if (keys) {
#              [...keys].forEach((key) => this.sendKey(key));
#            }
#          },
#          connectWebsocket: function () {
#            if (this.glvSocket !== null && this.glvSocket.readyState == 1) {
#              this.glvSocket.close();
#              return;
#            }
#    
#            const host = this.socketHost;
#            const port = this.socketPort;
#            const addr = `ws:\/\/${host}:${port}`;
#    
#            console.log(`trying to connect websocket to ${addr}`);
#            this.glvSocket = new WebSocket(addr);
#    
#            this.glvSocket.addEventListener("open", (event) => {
#              const url = event.target.url;
#              this.connectWebsocketButtonLabel = "Disconnect";
#              console.log(`connected websocket to ${url}`);
#            });
#    
#            this.glvSocket.addEventListener("close", (event) => {
#              this.connectWebsocketButtonLabel = "Connect";
#              console.log("disconnected");
#            });
#    
#            var q = this.glvSocketQueue;
#            this.glvSocket.addEventListener("message", async (event) => {
#              this.glvSocketQueue.push(event.data);
#            });
#          },
#          sendKey: function (k) {
#            this.glv.sendKey(k);
#          },
#          toggleFullscreen: function () {
#            if (!this.fullScreenMode) {
#              const elem = document.getElementById("app");
#              if (elem.requestFullscreen) {
#                elem.requestFullscreen();
#                this.fullScreenMode = true;
#              }
#            } else {
#              document.exitFullscreen();
#              this.fullScreenMode = false;
#            }
#          },
#          selectLocalFile: function () {
#            this.$refs.fileUpload.click();
#            if (!this.touchDevice) {
#              this.menuActive = false;
#            }
#          },
#          openLocalFile: async function (event) {
#            this.glvIsLoading = true;
#            await this.glv.loadStream(event);
#            this.glvIsLoading = false;
#          },
#          onDoubleTap: function (event) {
#            this.glvStreamIsPaused = !this.glvStreamIsPaused;
#          },
#        },
#      });
#    </script>
#    """, width=width, height=height)

def my_test(k='', width=800, height=600, key=None):
    # GLVis/glvis-js code, see included LICENSE.glvis-js BSD3 License
    components.html(f"""
    <p>My Test</p>
    <script src="https://glvis.org/live/src/glvis.js"></script>
    <script src="https://glvis.org/live/src/index.js"></script>
    <script src="https://glvis.org/live/src/helper.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/GLVis/glvis-js/examples/example_stream.js"></script>
    <div id="keys-div">Hello</div>
    <div id="glvis-div">GLVis not rendered</div>
    <script>
        document.getElementById("glvis-div").innerHTML = "BYE3";
        var div = document.getElementById("glvis-div");
        div.innerHTML = "";
        var glv = new glvis.State(div);
        glv.displayStream(example_stream + "keys {k}");
    </script>
    <div align="center">
        <input type="file" id="load_stream" onchange="glv.loadStream(event)" />
    </div>
    """, width=width, height=height)

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run streamlit_glvis/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.subheader("Component with constant args")
    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    num_clicks = streamlit_glvis("World")
    st.markdown("You've clicked %s times!" % int(num_clicks))

    st.markdown("---")
    st.subheader("Component with variable args")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    name_input = st.text_input("Enter a name", value="Streamlit")
    num_clicks = streamlit_glvis(name_input, key="foo")
    st.markdown("You've clicked %s times!" % int(num_clicks))
    st.markdown("---")
    k = st.text_input("GLVis keys")
    my_test(k=k)
    st.markdown("---")
    #glvis(name='hello')
