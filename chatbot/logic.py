from chatterbot.logic import LogicAdapter
from chatterbot import filters
from chatterbot.conversation import Statement
from chatbot.constants import BOT_NO_MORE_ANSWERS, BOT_NO_QUESTION


class BestMatch(LogicAdapter):
    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        self.excluded_words = kwargs.get('excluded_words')
        self.cached_responses = []

    def process(self, input_statement, additional_response_selection_parameters=None):
        # if an alternate response is requested,
        # just return it from the list of cached responses
        if input_statement.text.startswith("ALT_RESPONSE"):
            self.chatbot.logger.info(f"Alternate response requested. "
                                     f"Currently there are {len(self.cached_responses)} cached responses.")

            # if there are no cached responses,
            if self.cached_responses is None:
                # the user hasn't asked a question
                return Statement(BOT_NO_QUESTION)
            # if there are,
            else:
                # a response from the list can be returned
                # pop() removes it from the list
                try:
                    # the original response is stored at index 0
                    # the alternate responses start at index 1
                    return self.cached_responses.pop(1)
                # this exception is raised when there are no responses
                # at index 1 of the cache
                except IndexError:
                    # therefore there are no more known responses.
                    # let the user know
                    return Statement(BOT_NO_MORE_ANSWERS)

        search_results = self.search_algorithm.search(input_statement)

        # Use the input statement as the closest match if no other results are found
        closest_match = next(search_results, input_statement)

        # Search for the closest match to the input statement
        for result in search_results:
            # Stop searching if a match that is close enough is found
            if result.confidence >= self.maximum_similarity_threshold:
                closest_match = result
                break

        self.chatbot.logger.info('Using "{}" as a close match to "{}" with a confidence of {}'.format(
            closest_match.text, input_statement.text, closest_match.confidence
        ))

        recent_repeated_responses = filters.get_recent_repeated_responses(
            self.chatbot,
            input_statement.conversation
        )

        for index, recent_repeated_response in enumerate(recent_repeated_responses):
            self.chatbot.logger.info('{}. Excluding recent repeated response of "{}"'.format(
                index, recent_repeated_response
            ))

        response_selection_parameters = {
            'search_in_response_to': closest_match.search_text,
            'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words,
        }

        alternate_response_selection_parameters = {
            'search_in_response_to': self.chatbot.storage.tagger.get_bigram_pair_string(
                input_statement.text
            ),
            'exclude_text': recent_repeated_responses,
            'exclude_text_words': self.excluded_words,
        }

        if additional_response_selection_parameters:
            response_selection_parameters.update(additional_response_selection_parameters)
            alternate_response_selection_parameters.update(additional_response_selection_parameters)

        # Get all statements that are in response to the closest match
        response_list = list(self.chatbot.storage.filter(**response_selection_parameters))

        alternate_response_list = []

        if not response_list:
            self.chatbot.logger.info('No responses found. Generating alternate response list.')
            alternate_response_list = list(self.chatbot.storage.filter(**alternate_response_selection_parameters))
            self.cached_responses = alternate_response_list

        if response_list:
            self.chatbot.logger.info(
                'Selecting response from {} optimal responses.'.format(
                    len(response_list)
                )
            )
            self.cached_responses = response_list

            response = self.select_response(
                input_statement,
                response_list,
                self.chatbot.storage
            )

            response.confidence = closest_match.confidence
            self.chatbot.logger.info('Response selected. Using "{}"'.format(response.text))
        elif alternate_response_list:
            '''
            The case where there was no responses returned for the selected match
            but a value exists for the statement the match is in response to.
            '''
            self.chatbot.logger.info(
                'Selecting response from {} optimal alternate responses.'.format(
                    len(alternate_response_list)
                )
            )
            response = self.select_response(
                input_statement,
                alternate_response_list,
                self.chatbot.storage
            )

            response.confidence = closest_match.confidence
            self.cached_responses = alternate_response_list
            self.chatbot.logger.info('Alternate response selected. Using "{}"'.format(response.text))
        else:
            response = self.get_default_response(input_statement)

        self.chatbot.logger.warning(f"RESPONSE WITH ID {response.id} SELECTED")
        return response


class SpecificResponseAdapter(LogicAdapter):
    # Return a specific response to a specific input.

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        from chatterbot.conversation import Statement

        self.input_text = kwargs.get('input_text')

        output_text = kwargs.get('output_text')
        self.response_statement = Statement(text=output_text)

    def can_process(self, statement):
        # make the adapter case-insensitive
        # e.g. if "HeLp" is the input statement
        # the adapter should be able to process it
        # as if it were "help"
        if statement.text.lower() == self.input_text.lower():
            return True

        return False

    def process(self, statement, additional_response_selection_parameters=None):

        if statement.text.lower() == self.input_text.lower():
            self.response_statement.confidence = 1
        else:
            self.response_statement.confidence = 0

        return self.response_statement
