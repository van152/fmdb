char __fastcall sub_144500DE0(__int64 a1, __int64 a2, __int64 a3, __int64 a4, unsigned __int8 a5)
{
  __int64 v7; // [rsp+38h] [rbp-10h] BYREF

  v7 = *(_QWORD *)(a1 + 24);
  if ( (unsigned __int8)sub_140F7EE40(a3, (unsigned int)&v7, *(_QWORD *)(a3 + 152), a5, 1, 0) != 0 )
    *(_QWORD *)(a1 + 24) = v7;
  return 1;
}
