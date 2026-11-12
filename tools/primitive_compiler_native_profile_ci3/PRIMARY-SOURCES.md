# Primary Linux API basis

Read on 2026-10-17 (Asia/Shanghai); technical environment evidence only.

The [memory interface specification](https://docs.kernel.org/admin-guide/cgroup-v2.html#memory-interface-files) describes memory.current, memory.max and memory.events as interfaces that “exists on non-root cgroups”. [Conventions](https://docs.kernel.org/admin-guide/cgroup-v2.html#conventions) exempts the real root from resource controls. [The Root and Views](https://docs.kernel.org/admin-guide/cgroup-v2.html#the-root-and-views) distinguishes the initial namespace's real root from a namespace-relative root. [Interaction with Other Namespaces](https://docs.kernel.org/admin-guide/cgroup-v2.html#interaction-with-other-namespaces) explains namespace-relative cgroupfs mounts. Therefore mount-root text alone cannot justify omitting hidden ancestors.

The narrow implementation recognition used here is independently checked against upstream Linux v6.12, not inferred from runner conventions:

- [include/linux/proc_ns.h, PROC_CGROUP_INIT_INO](https://github.com/torvalds/linux/blob/v6.12/include/linux/proc_ns.h): reserved value 0xEFFFFFFB (4026531835).
- [kernel/cgroup/cgroup.c, init_cgroup_ns](https://github.com/torvalds/linux/blob/v6.12/kernel/cgroup/cgroup.c): initializes that namespace's inode with the reserved constant and its root with init_css_set.
- [kernel/cgroup/namespace.c, alloc_cgroup_ns and cgroupns_get](https://github.com/torvalds/linux/blob/v6.12/kernel/cgroup/namespace.c): newly allocated namespaces use ns_alloc_inum; task namespace lookup supplies the actual task cgroup namespace.
- [include/linux/proc_ns.h, ns_alloc_inum](https://github.com/torvalds/linux/blob/v6.12/include/linux/proc_ns.h) and [fs/proc/generic.c, proc_alloc_inum](https://github.com/torvalds/linux/blob/v6.12/fs/proc/generic.c): dynamic allocation starts at 0xF0000000, disjoint from the reserved initial identifier.
- [fs/nsfs.c, ns_get_name](https://github.com/torvalds/linux/blob/v6.12/fs/nsfs.c): the readlink target encodes namespace name and inode.

This is an explicit implementation fingerprint under the normal trusted-kernel/procfs assumption, not a stable-ABI promise, kernel-binary attestation, or proof against a malicious/fabricated OS interface. A different or inaccessible identifier is refused even when self and PID1 agree. The proposal does not claim a real Linux runner satisfied this recognition. Resource snapshots are non-atomic observations; they do not reserve memory or prevent concurrent consumption/migration. Per-child preflight remains necessary but is not a resource guarantee.
