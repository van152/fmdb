int *__fastcall sub_1444E1240(int *a1, _QWORD *a2, __int64 *a3)
{
  int v6; // eax
  __int64 v7; // rsi
  __int64 v8; // rbx
  __int64 v9; // rsi
  bool v10; // zf
  _DWORD v12[9]; // [rsp+24h] [rbp-24h] BYREF

  v12[0] = (unsigned __int64)(a3[1] - *a3) >> 3;
  (*(void (__fastcall **)(_QWORD, _DWORD *, __int64))(*(_QWORD *)*a2 + 40LL))(*a2, v12, 4);
  v6 = *(_DWORD *)(*a2 + 16LL);
  if ( v6 == 0 )
  {
    v7 = *a3;
    v8 = a3[1];
    if ( v7 != v8 )
    {
      v9 = v7 + 8;
      while ( (unsigned __int8)sub_1414A8C20(*(_QWORD *)(v9 - 8), a2) != 0 )
      {
        v6 = *(_DWORD *)(*a2 + 16LL);
        if ( v6 == 0 )
        {
          v10 = v9 == v8;
          v9 += 8;
          if ( !v10 )
            continue;
        }
        goto LABEL_9;
      }
      v6 = 1;
    }
  }
LABEL_9:
  *a1 = v6;
  return a1;
}
