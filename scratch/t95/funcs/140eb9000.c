char __fastcall sub_140EB9000(_QWORD *a1, __int64 a2, _QWORD *a3, char a4, unsigned __int8 a5)
{
  _QWORD *v7; // r13
  _QWORD *v8; // r12
  _QWORD *v9; // rbx
  _QWORD *v10; // rbp
  __int64 v11; // rbp
  __int64 v12; // rbp
  __int64 v13; // rcx
  __int64 v14; // rax
  __int64 v15; // rbx
  bool v16; // cf
  __int64 v17; // rdi
  _QWORD *v18; // rbp
  __int64 v19; // rbp
  _QWORD v22[9]; // [rsp+40h] [rbp-48h] BYREF

  sub_140F7F220(a3, a1 + 11, a5);
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 96, a3[5], a5, 1, 0);
  sub_140F7EE40((_DWORD)a3, (_DWORD)a1 + 112, a3[2], a5, 1, 0);
  v7 = a1 + 16;
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 128, a3[1], a5, 1, 0);
  v8 = a1 + 17;
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 136, a3[1], a5, 1, 0);
  v9 = a1 + 18;
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 144, a3[1], a5, 1, 0);
  v10 = a1 + 19;
  sub_140F7EC80((_DWORD)a3, (_DWORD)a1 + 152, a3[1], a5, 1, 0);
  if ( (unsigned __int8)sub_140F7EC80((_DWORD)a3, (int)a1 + 104, a3[3], a5, 1, 0) != 0 && (_QWORD *)a1[13] == a1 )
    a1[13] = 0;
  if ( *v7 != 0 && *(float *)(*v7 + 72LL) == 0.0 )
    *v7 = 0;
  if ( *v8 != 0 && *(float *)(*v8 + 72LL) == 0.0 )
    *v8 = 0;
  if ( *v10 != 0 && *(float *)(*v10 + 76LL) == 0.0 )
    *v10 = 0;
  if ( *v9 != 0 && *(float *)(*v9 + 76LL) == 0.0 )
    *v9 = 0;
  v11 = a1[26];
  if ( v11 != 0 )
  {
    sub_140F7FE40(&qword_141B5FDA8, a1[26], a5);
    sub_140F7FE40(&qword_141B5FDA8, v11 + 8, a5);
  }
  v12 = a1[27];
  if ( v12 != 0 )
  {
    sub_140F7FE40(&qword_141B5FDA8, a1[27], a5);
    sub_140F7FE40(&qword_141B5FDA8, v12 + 8, a5);
  }
  if ( a4 != 0 )
  {
    v22[0] = a1[23];
    if ( (unsigned __int8)sub_140F7EE40((_DWORD)a3, (unsigned int)v22, a3[19], a5, 1, 0) != 0 )
      a1[23] = v22[0];
    v13 = a1[21];
    if ( v13 != 0 )
      sub_1409FA760(v13, a5);
  }
  v14 = (a1[4] - a1[3]) >> 3;
  if ( (int)v14 > 0 )
  {
    v15 = (unsigned int)v14 + 1LL;
    do
    {
      v17 = (unsigned int)(v15 - 2);
      v18 = *(_QWORD **)(a1[3] + 8 * v17);
      v22[0] = *v18;
      if ( (unsigned __int8)sub_140F7EE40((unsigned int)&qword_141B5FDA8, (unsigned int)v22, qword_141B5FE40, a5, 1, 0) != 0 )
      {
        if ( v22[0] != 0 )
        {
          *v18 = v22[0];
        }
        else
        {
          v19 = a1[3];
          if ( *(_QWORD *)(v19 + 8 * v17) != 0 )
            sub_14007ADB0();
          sub_141758A00(v19 + 8 * v17, v19 + 8 * v17 + 8, a1[4] - (v19 + 8 * v17 + 8));
          a1[4] -= 8LL;
        }
      }
      v16 = v15-- == 1;
    }
    while ( !v16 && v15 != 1 );
  }
  return 1;
}
