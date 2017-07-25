/* Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid
 *
 * Licensed under the Apache License, Version 2.0 (the "License")
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import test from 'tape';
import React from 'react';
import ShallowRenderer from 'react-test-renderer/shallow';
import {App} from '../js/app.js';
import {Loader} from '../js/widgets/loader.js';


class EmptyStorage {
    getItem(key) {
        return null;
    }

    setItem(key, value) {
        return;
    }
}


test('app', function(t) {
    const renderer = new ShallowRenderer();
    renderer.render(<App storage={new EmptyStorage()}/>);
    const result = renderer.getRenderOutput();
    t.equals(result.type, 'div');
    t.end();
});

test('app starts loading', function(t) {
    const renderer = new ShallowRenderer();
    renderer.render(<App storage={new EmptyStorage()}/>);
    const result = renderer.getRenderOutput();
    t.comment(Object.keys(result.props));
    t.deepEquals(result.props.children.props.children.props.children, <Loader/>);
    t.end();
});