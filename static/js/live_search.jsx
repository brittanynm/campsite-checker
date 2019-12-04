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
                <div className="custom-control custom-checkbox" key={key}>
                    <input  type="checkbox" 
                            className="form-check-input" 
                            name="selected_site" 
                             
                            value={campsite.id}/>

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
            <div className="container-fluid">
                    <div className="row"> 
                        <div className="col">
                            <div className="name-sidebar">
                                <form 
                                    onSubmit={this.submitHandler} 
                                    className="form-inline" 
                                    method = "GET" 
                                    action="/search">
                                    <div className="form-group">
                                        <label id="search-title" htmlFor="query"><h3>Where do you want to go?</h3>
                                        </label>
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
                    </div>

                    <div className="row">
                        <div className="col">
                            <form className="form-inline-2" method = "POST" action="/search">
                                <div className="list" id="campsite_list">
                                    {this.renderCampsites()}
                                    <div className="text-right">
                                        <button type="submit" className = "btn-selection">Next > 
                                        </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
            </div>
        );
    }
}

ReactDOM.render(
    <CampsiteSearch />, 
    $('#root')[0]
);