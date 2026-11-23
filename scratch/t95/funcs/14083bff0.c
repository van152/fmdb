_QWORD *__fastcall sub_14083BFF0(_QWORD *a1, _QWORD *a2)
{
  _QWORD *v3; // r14
  _QWORD *v4; // rdi
  void (__fastcall *v5)(__int64, _QWORD *); // r13
  _QWORD *v6; // r15
  _QWORD *v7; // rsi
  __int64 v8; // rcx
  __int64 v9; // rbx
  __int64 v10; // rsi
  _QWORD *v12; // [rsp+28h] [rbp-8h]

  if ( a1 != a2 )
  {
    v3 = (_QWORD *)*a1;
    v4 = (_QWORD *)a1[1];
    if ( (_QWORD *)*a1 != v4 )
    {
      v12 = a2;
      v5 = (void (__fastcall *)(__int64, _QWORD *))MEMORY[0x1419475D8];
      v6 = (_QWORD *)*a1;
      do
      {
        v7 = (_QWORD *)*v6;
        if ( *v6 != 0 )
        {
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*v7 + 16LL))(*v7, *v6);
          v9 = sub_140836BC0(v8);
          v5(v9 + 32, v7);
          if ( (*(_BYTE *)(v9 + 72) == 0 || _InterlockedDecrement((volatile signed __int32 *)(v9 + 64)) == 0)
            && *(_BYTE *)(v9 + 97) != 0 )
          {
            sub_1412D33C0(v9);
          }
        }
        ++v6;
      }
      while ( v6 != v4 );
      v10 = a1[1] - (_QWORD)v4;
      sub_141758A00();
      a1[1] = (char *)v3 + v10;
      a2 = v12;
    }
    sub_14083C860(a1, a2);
  }
  return a1;
}
