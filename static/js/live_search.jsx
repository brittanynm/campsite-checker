class CampsiteSearch extends React.Component {
    constructor() {
        super();
        this.state = {
            campsites: {},
            inputValue: ''
        };
        this.handleSearchChange = this.handleSearchChange.bind(this);
    }

    componentDidMount() {
        $.get('/live_search', {query: ''}, (data) => {
            this.setState({ campsites: data });
        });
    }

    handleSearchChange(evt) {
        this.setState({ inputValue: evt.target.value });

        $.get('/live_search', {query: evt.target.value}, (data) => {
            this.setState({ campsites: data });
        });
    }

    renderCampsites() {
        const campsiteDivs = [];

        for (const [key, campsite] of Object.entries(this.state.campsites)) {
            campsiteDivs.push(
                <div className="campsite-name" key={key}>
                    <input type="checkbox" name="selected_site" value={campsite.id}/>
                    <b> {campsite.name} </b>
                    {campsite.park}<hr />
                </div>
            );
        }

        return campsiteDivs;
    }
    
    submitHandler(evt) {
        evt.preventDefault();
    }

    render() {
        return (
            <div>
                <div className="col-sm-3 col-sm-offset-1 name-sidebar">
                    <div className="sidebar-module sidebar-module-inset">
                    <br /><br />
                        <form 
                            onSubmit={this.submitHandler} 
                            className="form-inline" 
                            method = "GET" 
                            action="/search"
                            >
                            <div className="form-group">
                                <label htmlFor="query">Where do you want to go? </label>
                                <input
                                    type="text"
                                    name="query"
                                    className="form-control"
                                    id="query"
                                    value={this.state.query}
                                    onChange={this.handleSearchChange}
                                />
                            </div>

                            {/* <button type="submit" className="btn btn-primary">Search</button><br /><br />*/}
                        </form><br /><br />
                        
                    </div>
                </div>

                <div>
    <form className="form-inline-2" method = "POST" action="/search">
        <div className="list" id="campsite_list">
            {this.renderCampsites()}
            <button type="submit" className = "btn btn-selection">Next > </button>
            <br /><br />
           </div>
    </form>

</div>
            </div>
        );
    }
}

ReactDOM.render(
    <CampsiteSearch />, 
    $('#root')[0]
);