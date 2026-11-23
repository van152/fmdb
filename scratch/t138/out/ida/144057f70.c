__int64 sub_144057F70()
{
  __int64 v0; // rax

  sub_14080D0E0(a1: &unk_141B62038, a2: 0x1418E2C24LL);
  v0 = sub_1412EC810(a1: 264, a2: 12);
  *(_QWORD *)v0 = 0xC00000000LL;
  strcpy((char *)(v0 + 8), "memory_pools");
  _InterlockedIncrement((volatile signed __int32 *)v0);
  qword_141B62040 = 0;
  _InterlockedIncrement((volatile signed __int32 *)v0);
  qword_141B62040 = v0 + 4;
  if ( _InterlockedDecrement((volatile signed __int32 *)v0) == 0 )
    sub_1412EC9A0(a1: v0);
  return sub_141751048(a1: sub_141213530);
}
