class Handler{
	constructor(all_qs){
		this.all_questions = all_qs
		this.previous_question = null
		this.previous_question_answered = false
		this.question_answers = new Array();
		this.score = 0
		this.failed = 0
		this.answered_questions = new Array();
	}
	
	get_question(){

		let random_index = Math.floor(Math.random() * this.all_questions.length);
		question = this.all_questions[random_index]
		
		return question
	}

	get_answer(){
		let answer_buttons = document.getElementsClassName('answer-button');
		for(let i=0; i < answer_buttons.length; i++){
			answer_buttons[i].addEventListener("click");
		}
	}


	store_info(){
		let json_object = {};
		json_object["all_questions"] = this.all_questions
		json_object[""]
	}
}