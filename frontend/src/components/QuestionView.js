import React, { Component } from 'react';

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

const backendRoute = process.env.REACT_APP_BACKEND_URL;

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: [],
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `${backendRoute}/questions?page=${this.state.page}`, //DONETODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.list_of_questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.categories[0]
        })
        // console.log(result)
        // console.log(result.categories[2].type.toLowerCase())
        console.log(this.state.categories)
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  createPagination(){
    let pageNumbers = [];
    let maxPage = Math.ceil(this.state.totalQuestions / 10)
    for (let i = 1; i <= maxPage; i++) {
      pageNumbers.push(
        <span
          key={i}
          className={`page-num ${i === this.state.page ? 'active' : ''}`}
          onClick={() => {this.selectPage(i)}}>{i}
        </span>)
    }
    return pageNumbers;
  }

  getByCategory= (id) => {
    $.ajax({
      url: `${backendRoute}/categories/${id}/questions`, //DONETODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `${backendRoute}/questions?search=${searchTerm}`, //DONETODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({search: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: this.state.currentCategory })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `${backendRoute}/questions/${id}`, //DONETODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    return (
      <div className="question-view">
        <div className="categories-list">
          <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
          <ul>
            {
              this.state.categories.map((category) => (
                <li key={category.id} onClick={()=> {this.getByCategory(category.id)}}>
                  {category.type}
                  <img src={category.type.toLowerCase() + ".svg"} alt="" className="category" />
                </li>
              ))
            }
            
          </ul>
          <Search submitSearch={this.submitSearch}/>
        </div>
        <div className="questions-list">
          <h2>Questions</h2>
          {this.state.questions.map((q, ind) => (
            <Question
              key={q.id}
              question={q.question}
              answer={q.answer}
              category={this.state.categories[q.category -1]} 
              difficulty={q.difficulty}
              questionAction={this.questionAction(q.id)}
            />
          ))}
          <div className="pagination-menu">
            {this.createPagination()}
          </div>
        </div>

      </div>
    );
  }
}

export default QuestionView;
