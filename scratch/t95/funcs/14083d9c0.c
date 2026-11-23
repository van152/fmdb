_QWORD *__fastcall sub_14083D9C0(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rdi
  __int64 v5; // rcx
  __int64 v6; // rcx
  __int64 v8[5]; // [rsp+20h] [rbp-28h] BYREF

  v4 = sub_14083D4F0(a1);
  v8[0] = 0;
  sub_140809040(v8, a2, -1);
  a1[1] = 0;
  if ( a1 + 1 != v8 )
  {
    v5 = v8[0];
    if ( v8[0] != 0 )
      _InterlockedIncrement((volatile signed __int32 *)(v8[0] - 4));
    a1[1] = v5;
  }
  *a1 = v4 + 136;
  v6 = v8[0];
  if ( v8[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v8[0] - 4)) == 0 )
    sub_1412EC9A0(v6 - 4);
  return a1;
}
