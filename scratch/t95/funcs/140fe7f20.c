__int64 *__fastcall sub_140FE7F20(__int64 a1, __int64 *a2)
{
  int v3; // ebx
  __int64 v4; // r9
  _DWORD **v5; // rcx
  int v6; // eax
  int v7; // ecx
  __int64 *v8; // rdi
  __int64 v9; // rdx
  __int64 v10; // rdi
  _DWORD *v11; // rdi
  int v12; // eax
  __int64 v13; // rax
  bool v14; // zf
  int v16; // [rsp+28h] [rbp-20h] BYREF
  int v17; // [rsp+2Ch] [rbp-1Ch]

  if ( (*(_BYTE *)(qword_141B5FE08 + 90) & 4) == 0 )
  {
    v3 = -1;
    if ( (int)a1 < 0 )
      goto LABEL_26;
    if ( qword_141B5FE10 != 0 )
    {
      if ( (_BYTE)word_141B60320 == 0 )
      {
        v4 = *(_QWORD *)(qword_141B5FE10 + 96);
        if ( (*(_QWORD *)(qword_141B5FE10 + 104) - v4) >> 3 > (unsigned __int64)(unsigned int)a1 )
        {
          v5 = (_DWORD **)(v4 + 8LL * (unsigned int)a1);
          goto LABEL_16;
        }
      }
      v8 = *(__int64 **)(qword_141B5FE10 + 128);
      v9 = *v8;
      v10 = v8[1] - *v8;
      if ( v10 != 0 && v10 >> 3 > (unsigned __int64)(unsigned int)a1 )
      {
        v5 = (_DWORD **)(v9 + 8LL * (unsigned int)a1);
LABEL_16:
        v11 = *v5;
        if ( (_BYTE)word_141B60320 == 0 )
          goto LABEL_17;
LABEL_20:
        if ( v11 != nullptr )
        {
          v13 = (*(__int64 (__fastcall **)(_DWORD *))(*(_QWORD *)v11 + 1816LL))(v11);
          if ( v13 != 0 )
          {
            v14 = (*(_BYTE *)(v13 + 103) & 8) == 0;
            v12 = -1;
            if ( !v14 )
              goto LABEL_27;
          }
          goto LABEL_23;
        }
LABEL_26:
        v12 = -1;
LABEL_27:
        v16 = v3;
        v17 = v12;
        return sub_140FE72B0(&v16, 1348825715, a2);
      }
    }
    v11 = nullptr;
    if ( (_BYTE)word_141B60320 == 0 )
    {
LABEL_17:
      v12 = -1;
      if ( v11 == nullptr )
        goto LABEL_27;
LABEL_23:
      v3 = v11[3];
      v12 = v11[4];
      if ( v12 == 0 )
        v12 = v11[3];
      goto LABEL_27;
    }
    goto LABEL_20;
  }
  if ( a1 != 0 )
  {
    v6 = *(_DWORD *)(a1 + 12);
    v7 = *(_DWORD *)(a1 + 16);
    if ( v7 == 0 )
      v7 = v6;
  }
  else
  {
    v6 = -1;
    v7 = -1;
  }
  v16 = v6;
  v17 = v7;
  return sub_140FE72B0(&v16, 1348825715, a2);
}
