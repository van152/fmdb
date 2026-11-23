char __fastcall sub_143C01800(__int64 a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // rax

  sub_140F7F220(a3, a1 + 80, a5);
  sub_140F7EC80(a3, a1 + 96, *(_QWORD *)(a3 + 40), a5, 1, 0);
  sub_140F7EC80(a3, a1 + 88, *(_QWORD *)(a3 + 24), a5, 1, 0);
  sub_140F7F730(a3, a1 + 104, a5);
  v7 = *(_QWORD *)(a1 + 88);
  if ( v7 != 0 && *(_DWORD *)(v7 + 12) == 100000023 )
  {
    *(_BYTE *)(a1 + 131) = 6;
    if ( *(_BYTE *)(a1 + 137) == 8 )
      *(_BYTE *)(a1 + 137) = 7;
  }
  return 1;
}
