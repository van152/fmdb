bool __fastcall sub_14447E060(__int16 *a1, _QWORD *a2)
{
  __int64 v4; // r8
  _QWORD *v5; // r12
  __int64 v6; // r8
  bool v7; // zf
  _QWORD *v8; // rdi
  int v9; // eax
  int v10; // eax
  int v11; // eax
  unsigned __int64 i; // rbx
  unsigned int v14; // [rsp+2Ch] [rbp-3Ch] BYREF
  _DWORD v15[14]; // [rsp+30h] [rbp-38h] BYREF

  v4 = a2[2];
  if ( (unsigned int *)a2[3] == &v14 )
  {
    v5 = a2 + 2;
    v7 = v4 == -4;
    v6 = v4 + 4;
    a2[2] = v6;
    a2[3] = v15;
    if ( v7 )
      goto LABEL_9;
  }
  else
  {
    if ( v4 != 0 && *a2 != 0 )
      (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1]);
    a2[1] = &v14;
    v5 = a2 + 2;
    a2[2] = 4;
    a2[3] = v15;
    v6 = 4;
  }
  if ( *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD, __int64))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: a2[1], a3: v6);
LABEL_9:
  v8 = a2 + 1;
  a2[3] = 0;
  a2[2] = 0;
  a2[1] = 0;
  if ( v14 != 0 )
  {
    sub_1414E5A30(a1, a2);
    v9 = *a1;
    if ( v9 < -1
      || (__int16)((unsigned int)(*(_DWORD *)(*(_QWORD *)(qword_141B5FDE8 + 128) + 8LL)
                                - **(_DWORD **)(qword_141B5FDE8 + 128)) >> 3) <= v9 )
    {
      *(_DWORD *)a1 = -1073676289;
    }
    if ( v14 >= 2 )
    {
      if ( *v5 != 0 && *a2 != 0 )
        (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v8);
      a2[3] = 0;
      a2[2] = 0;
      *v8 = 0;
      sub_1414E5A30(a1: a1 + 2, a2);
      v10 = a1[2];
      if ( v10 < -1
        || (__int16)((unsigned int)(*(_DWORD *)(*(_QWORD *)(qword_141B5FDE8 + 128) + 8LL)
                                  - **(_DWORD **)(qword_141B5FDE8 + 128)) >> 3) <= v10 )
      {
        *((_DWORD *)a1 + 1) = -1073676289;
      }
      if ( v14 >= 3 )
      {
        if ( *v5 != 0 && *a2 != 0 )
          (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v8);
        a2[3] = 0;
        a2[2] = 0;
        *v8 = 0;
        sub_1414E5A30(a1: a1 + 4, a2);
        v11 = a1[4];
        if ( v11 < -1
          || (__int16)((unsigned int)(*(_DWORD *)(*(_QWORD *)(qword_141B5FDE8 + 128) + 8LL)
                                    - **(_DWORD **)(qword_141B5FDE8 + 128)) >> 3) <= v11 )
        {
          *((_DWORD *)a1 + 2) = -1073676289;
        }
        if ( v14 >= 4 )
        {
          for ( i = 3; i < v14; ++i )
          {
            v15[0] = -1073676289;
            if ( *v5 != 0 && *a2 != 0 )
              (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v8);
            a2[3] = 0;
            a2[2] = 0;
            *v8 = 0;
            sub_1414E5A30(a1: v15, a2);
          }
        }
      }
    }
  }
  if ( *v5 != 0 && *a2 != 0 )
    (*(void (__fastcall **)(_QWORD, _QWORD))(*(_QWORD *)*a2 + 40LL))(a1: *a2, a2: *v8);
  a2[3] = 0;
  a2[2] = 0;
  *v8 = 0;
  return *(_DWORD *)(*a2 + 16LL) == 0;
}
