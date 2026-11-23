char __fastcall sub_143C10EA0(__int64 a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // rbx

  v7 = a1 + 32;
  if ( (unsigned __int8)sub_140F7EC80(a3, (int)a1 + 32, *(_QWORD *)(a3 + 40), a5, 1, 0) != 0 && *(_QWORD *)v7 != 0 )
    ++*(_DWORD *)(*(_QWORD *)v7 + 376LL);
  sub_140F80050(a3, a1 + 40, a5);
  sub_140F7EC80(a3, a1 + 48, *(_QWORD *)(a3 + 80), a5, 1, 0);
  sub_140F7F730(a3, a1 + 56, a5);
  return 1;
}
