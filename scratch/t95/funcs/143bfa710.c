_QWORD *__fastcall sub_143BFA710(_QWORD **a1, __int16 a2)
{
  _QWORD *result; // rax
  __int64 v3; // rbp
  __int64 v5; // rdi
  __int64 v6; // rbp
  __int64 v7; // r13
  _QWORD *v8; // rsi
  __int64 *v9; // rbx
  __int64 v10; // rcx
  _QWORD **v11; // [rsp+20h] [rbp-48h]

  result = *a1;
  if ( *a1 != nullptr )
  {
    v3 = result[1] - *result;
    if ( v3 != 0 )
    {
      v5 = v3 >> 3;
      v6 = -(__int64)(v3 & 0xFFFFFFFFFFFFFFF8uLL);
      v11 = a1;
      do
      {
        v7 = v5 - 1;
        v8 = *a1;
        v9 = *(__int64 **)(**a1 + 8 * v5 - 8);
        if ( *((_WORD *)v9 + 4) == a2 )
        {
          v10 = *v9;
          if ( *v9 != 0 && _InterlockedDecrement((volatile signed __int32 *)(v10 - 4)) == 0 )
            sub_1412EC9A0(v10 - 4);
          sub_140E469C0(v9);
          result = (_QWORD *)sub_141758A00();
          v8[1] -= 8LL;
          a1 = v11;
        }
        v6 += 8;
        --v5;
      }
      while ( v7 != 0 );
    }
  }
  return result;
}
