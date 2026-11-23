char __fastcall sub_143FB6D00(__int64 a1, __int64 a2, __int64 a3, char a4, unsigned __int8 a5)
{
  if ( a4 != 0 )
  {
    sub_140F7EB80(a3, a1 + 24, a5);
    sub_140F80250(a3, a1 + 32, a5, 0);
    sub_140F80250(a3, a1 + 48, a5, 0);
    sub_140F80250(a3, a1 + 72, a5, 0);
    sub_140F7EC80(a3, a1 + 40, *(_QWORD *)(a3 + 40), a5, 1, 0);
    sub_140F7EC80(a3, a1 + 56, *(_QWORD *)(a3 + 40), a5, 1, 0);
    sub_140F7EC80(a3, a1 + 64, *(_QWORD *)(a3 + 40), a5, 1, 0);
  }
  return 1;
}
