import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import ReactDOM from 'react-dom'
//import glvis from "./glvis-js/glvis.js";
interface State {
  numClicks: number
  isFocused: boolean
}

/**
 * This is a React-based component template. The `render()` function is called
 * automatically when your component should be re-rendered.
 */
class StreamlitGLVis extends StreamlitComponentBase<State> {
  public streamlit_state = { numClicks: 0, isFocused: false }

  public render = (): ReactNode => {
    // Arguments that are passed to the plugin in Python are accessible
    // via `this.props.args`. Here, we access the "name" arg.
    const name = this.props.args["name"]
    const data = this.props.args["stream"]
    const width = this.props.args["width"]
    const height = this.props.args["height"]

    // Streamlit sends us a theme object via props that we can use to ensure
    // that our component has visuals that match the active theme in a
    // streamlit app.
    const { theme } = this.props
    const style: React.CSSProperties = {}

    // Maintain compatibility with older versions of Streamlit that don't send
    // a theme object.
    if (theme) {
      // Use the theme object to style our button border. Alternatively, the
      // theme style is defined in CSS vars.
      const borderStyling = `1px solid ${
        this.streamlit_state.isFocused ? theme.primaryColor : "gray"
      }`
      style.border = borderStyling
      style.outline = borderStyling
    }

    var div = document.createElement("div")
    //var glv = new glvis.State(_State(), this.width, this.height)
    // Show a button and some text.
    // When the button is clicked, we'll increment our "numClicks" streamlit_state
    // variable, and send its new value back to Streamlit, where it'll
    // be available to the Python program.
    return (
      <span>
        <div>
            Hey, {name}! &nbsp;
            <button
              style={style}
              onClick={this.onClicked}
              disabled={this.props.disabled}
              onFocus={this._onFocus}
              onBlur={this._onBlur}>
              Click Me!
            </button>
        </div>
      </span>
    )
  }

  /** Click handler for our "Click Me!" button. */
  private onClicked = (): void => {
    // Increment streamlit_state.numClicks, and pass the new value back to
    // Streamlit via `Streamlit.setComponentValue`.
    this.setState(
      prevState => ({ numClicks: prevState.numClicks + 1 }),
      () => Streamlit.setComponentValue(this.streamlit_state.numClicks)
    )
  }

  /** Focus handler for our "Click Me!" button. */
  private _onFocus = (): void => {
    this.setState({ isFocused: true })
  }

  /** Blur handler for our "Click Me!" button. */
  private _onBlur = (): void => {
    this.setState({ isFocused: false })
  }

  private _State = (): void => {
    var screen = 0
    var innerWidth = 300
    var innerHeight = 400
    var event = new Object()
    var pageXOffset = 0
    var pageYOffset = 0
    var CanvasPixelArray = 0  
  }
}

// "withStreamlitConnection" is a wrapper function. It bootstraps the
// connection between your component and the Streamlit app, and handles
// passing arguments from Python -> Component.
//
// You don't need to edit withStreamlitConnection (but you're welcome to!).
export default withStreamlitConnection(StreamlitGLVis)
