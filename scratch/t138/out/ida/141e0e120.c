__int64 __fastcall sub_141E0E120(__int64 a1, __int64 a2)
{
  __int64 v4; // rcx
  __int64 v5; // rcx
  _BYTE v7[24]; // [rsp+20h] [rbp-18h] BYREF

  sub_1407D8AB0(a1: v7, a2: 0x1418E2C24LL);
  v4 = *(_QWORD *)(a1 + 44272);
  if ( v4 != 0 )
  {
    sub_1400DFF10(a1: v4, a2, a3: v7);
  }
  else
  {
    v5 = *(_QWORD *)(a1 + 44264);
    if ( v5 != 0 )
      sub_14120FDD0(a1: v5, a2, a3: v7);
  }
  return sub_140A2B000(a1, a2);
}
