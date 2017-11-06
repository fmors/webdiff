from flask import Blueprint, request, jsonify, make_response

MAX_NUMBER_OF_SESSIONS = 16

api = Blueprint('api_v1', __name__)
diff_sessions = {}


@api.route('/diff/<int:diff_id>', methods=['GET'])
def show_diff_id(diff_id):
    """
    Handle the endpoint to show the diff
    :param diff_id: id of the diff session
    :return: result of comparing left and right sides
    """
    # Validate parameters
    if diff_id not in diff_sessions:
        return make_response(jsonify({'error': 'Diff session ID not found'}), 404)

    if 'left' not in diff_sessions[diff_id]:
        return make_response(jsonify({'error': 'Left side missing'}), 400)

    if 'right' not in diff_sessions[diff_id]:
        return make_response(jsonify({'error': 'Right side missing'}), 400)

    left = diff_sessions[diff_id]['left']
    right = diff_sessions[diff_id]['right']

    # Do the diff
    return jsonify(compare_left_and_right(left, right))


@api.route('/diff/<int:diff_id>/<string:side>', methods=['POST'])
def post_diff_id_side(diff_id, side):
    """
    Handle the endpoint of setting each side for a given diff session. Posted data must be JSON containing a 'data' key
    :param diff_id: id of the diff session to be used. If does not exist, create session (up to max 16 sessions)
    :param side: side of the diff that this data belongs to
    :return: success message or error message
    """
    # Validate parameters
    if diff_id not in diff_sessions:
        if len(diff_sessions) >= MAX_NUMBER_OF_SESSIONS:
            return make_response(
                jsonify({'error': 'Max number of diff sessions ({}) reached.'.format(MAX_NUMBER_OF_SESSIONS)}), 400)

    if side != 'left' and side != 'right':
        return make_response(jsonify({'error': 'Only left or right side accepted.'}), 400)

    if request.content_type != 'application/json':
        return make_response(jsonify({'error': 'Invalid data type: only \'application/json\' accepted'}), 400)

    if 'data' not in request.get_json():
        return make_response(jsonify({'error': 'No \'data\' received'}), 400)

    if not request.get_json().get('data'):
        return make_response(jsonify({'error': 'Empty \'data\' received'}), 400)

    # Post diff side
    if diff_id not in diff_sessions:
        diff_sessions.update({diff_id: {}})

    diff_sessions[diff_id][side] = bytes(request.get_json()['data'], encoding='utf-8')

    return jsonify({'result': 'Diff session {} {} side successfully set'.format(diff_id, side)})


def compare_left_and_right(left, right):
    """
    Function used to compare left and right sides of a diff. First compares left and right side lengths. If equal, then
    compare contents. If equal, just print a message. Otherwise, print each difference block offset and size.
    :param left:
    :param right:
    :return: result showing the difference (same contents, size differs or difference blocks with offset and size)
    """
    if len(left) != len(right):
        return {'result': 'Left and right sizes do not match'}

    differences = []
    equals = True
    for i in range(len(left)):
        if equals and left[i] != right[i]:
            equals = False
            differences.append({'offset': i, 'size': 1})
        elif not equals and left[i] != right[i]:
            differences[-1]['size'] += 1
        elif not equals and left[i] == right[i]:
            equals = True

    if differences:
        return {'result': 'Left and right contents do not match', 'differences': differences}

    return {'result': 'Left and right contents are the same'}
