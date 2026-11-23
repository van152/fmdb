char __fastcall sub_1415D5750(__int64 a1, int a2, __int64 *a3)
{
  __int64 v6; // rsi

  v6 = -*(_DWORD *)(a1 - 4);
  if ( (unsigned __int8)sub_140E27B10(a1: a1 + v6 - 240, a2, a3) != 0 )
    return 1;
  else
    return sub_140DCA880(a1: v6 + a1, a2, a3);
}
