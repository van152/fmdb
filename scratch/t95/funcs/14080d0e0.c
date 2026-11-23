_QWORD *__fastcall sub_14080D0E0(_QWORD *a1, __int64 a2)
{
  __int64 v4; // rbx
  __int64 v5; // rcx
  __int64 v7[6]; // [rsp+20h] [rbp-10h] BYREF

  v7[1] = -2;
  v4 = sub_140105F10() + 8;
  v7[0] = 0;
  sub_140809040(v7, a2, -1);
  *a1 = sub_14080D8E0(v4, v7);
  v5 = v7[0];
  if ( v7[0] != 0 && _InterlockedDecrement((volatile signed __int32 *)(v7[0] - 4)) == 0 )
    sub_1412EC9A0(v5 - 4);
  return a1;
}
