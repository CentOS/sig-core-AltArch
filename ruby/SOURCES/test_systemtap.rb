require 'set'

LIBRUBY_SO = 'libruby.so'
PROBES_D = 'probes.d'

###
# Detect SystemTap section headers presence.

stap_headers = [
  '\.stapsdt\.base',
  '\.note\.stapsdt'
]

header_regexp = %r{ (#{stap_headers.join('|')}) }

section_headers = `readelf -S "#{LIBRUBY_SO}"`
detected_stap_headers = section_headers.scan(header_regexp).flatten

# Assume there are both headers until this is proven wrong ;)
unless detected_stap_headers.size == 2
  puts 'ERROR: SystemTap (DTrace) headers were not detected in resulting library.'
  exit false
end

###
# Find if every declared probe is propagated to resulting library.

# Colect probes specified in probes.d file.
probes = []

File.open(PROBES_D) do |file|
  file.each_line do |line|
    if probe = line[/probe (\S+)\(.*\);/, 1]
      probes << probe
    end
  end
end

probes = Set.new probes

# These probes are excluded by VM_COLLECT_USAGE_DETAILS ifdef.
EXCLUDE_PROBES = Set.new %w(insn insn__operand)
unless EXCLUDE_PROBES.subset? probes
  puts 'ERROR: Change in SystemTap (DTrace) probes definition file detected.'
  exit false
end

probes -= EXCLUDE_PROBES

# Detect probes in resulting library.
probe_regexp = %r{
^\s*stapsdt\s*0[xX][0-9a-fA-F]+\tNT_STAPSDT \(SystemTap probe descriptors\)$
^\s*Provider: ruby$
^\s*Name: (\S+)$
}

notes = `readelf -n "#{LIBRUBY_SO}"`
detected_probes = Set.new notes.scan(probe_regexp).flatten

# Both sets must be equal, otherwise something is wrong.
unless probes == detected_probes
  puts 'ERROR: SystemTap (DTrace) probes were not correctly propagated into resulting library.'
  exit false
end
