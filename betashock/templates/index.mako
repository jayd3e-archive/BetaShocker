<%inherit file="layouts/base.mako"/>

<%def name="body()">
	<h2>STATS</h2>
	<table cellpadding="0" cellspacing="0">
		<tr>
			<th>Average Total Posts</th>
			<td>${avg_total_posts}</td>
		</tr>
		<tr>
			<th>Average Days of Membership</th>
			<td>${avg_days}</td>
		</tr>
	</table>
</%def>
